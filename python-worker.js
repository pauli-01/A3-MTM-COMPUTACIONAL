// O interpretador executa o arquivo Python em uma tarefa separada da interface.
import { loadPyodide } from './runtime/pyodide.mjs';

function prepararMatriz(matriz, nome) {
  return matriz.map((linha, i) => linha.map((valor, j) => {
    const local = `Matriz ${nome}, linha ${i + 1}, coluna ${j + 1}`;
    if (typeof valor === 'string') {
      const texto = valor.trim().replace(',', '.');
      if (!texto) throw new Error(`${local}: preencha este campo.`);
      if (!/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(texto)) {
        throw new Error(`${local}: use números, com vírgula ou ponto decimal.`);
      }
      valor = Number(texto);
    }
    if (typeof valor !== 'number') throw new Error(`${local}: digite um número válido.`);
    if (!Number.isFinite(valor) || Math.abs(valor) > 1_000_000_000_000) {
      throw new Error(`${local}: use um número entre −1 trilhão e 1 trilhão.`);
    }
    return valor;
  }));
}

function formatarNumero(valor) {
  if (typeof valor === 'bigint' || Number.isInteger(valor)) {
    return BigInt(valor).toString();
  }

  // Mantém até 12 algarismos significativos para valores fracionários.
  const [mantissa, potencia] = valor.toExponential(11).split('e');
  const expoente = Number(potencia);
  const cientifico = expoente < -4 || expoente >= 12;
  const decimal = cientifico ? mantissa : valor.toFixed(11 - expoente);
  const digitos = decimal.includes('.')
    ? decimal.replace(/0+$/, '').replace(/\.$/, '').replace('.', ',')
    : decimal;
  if (!cientifico) return digitos;

  const sinal = expoente < 0 ? '-' : '+';
  return `${digitos}e${sinal}${String(Math.abs(expoente)).padStart(2, '0')}`;
}

function prepararResposta(resposta) {
  const passos = resposta.passos.map((passo) => {
    const termos = passo.termos.map(({a, b, produto, acumulado}) => ({
      a: formatarNumero(a),
      b: formatarNumero(b),
      produto: formatarNumero(produto),
      acumulado: formatarNumero(acumulado),
    }));
    const valor = formatarNumero(passo.valor);
    const expressao = termos.map(({a, b}) => `(${a} × ${b})`).join(' + ') + ` = ${valor}`;
    return {...passo, termos, valor, expressao};
  });
  return {...resposta, passos};
}

const ready = (async () => {
  const pyodide = await loadPyodide({indexURL: new URL('./runtime/', import.meta.url).href});
  const response = await fetch(new URL('./cod-mult-matriz.py', import.meta.url));
  if (!response.ok) throw new Error('Código Python indisponível.');
  pyodide.runPython(await response.text());
  const multiplicar = pyodide.globals.get('multiplicar_matrizes');
  self.postMessage({type: 'ready'});
  return {pyodide, multiplicar};
})();

ready.catch(() => self.postMessage({type: 'init-error'}));
self.onmessage = async ({data}) => {
  const {id} = data;
  let matrizes;
  try {
    const {a, b} = JSON.parse(data.json);
    matrizes = [prepararMatriz(a, 'A'), prepararMatriz(b, 'B')];
  } catch (error) {
    self.postMessage({id, ok: false, erro: error.message});
    return;
  }

  const proxies = [];
  try {
    const {pyodide, multiplicar} = await ready;
    for (const matriz of matrizes) proxies.push(pyodide.toPy(matriz));
    const resultado = multiplicar(...proxies);
    proxies.push(resultado);
    const resposta = resultado.toJs({dict_converter: Object.fromEntries, create_pyproxies: false});
    if (resposta.erro) {
      self.postMessage({id, ok: false, erro: resposta.erro});
    } else {
      self.postMessage({id, ok: true, dados: prepararResposta(resposta)});
    }
  } catch {
    self.postMessage({id, ok: false, erro: 'Não foi possível executar o Python. Atualize a página para tentar novamente.'});
  } finally {
    for (const proxy of proxies) proxy.destroy();
  }
};
