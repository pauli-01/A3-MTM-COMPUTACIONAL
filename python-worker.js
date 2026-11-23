// O interpretador executa o arquivo Python em uma tarefa separada da interface.
import { loadPyodide } from './runtime/pyodide.mjs';

const ready = (async () => {
  const pyodide = await loadPyodide({indexURL: new URL('./runtime/', import.meta.url).href});
  const response = await fetch(new URL('./cod-mult-matriz.py', import.meta.url));
  if (!response.ok) throw new Error('Código Python indisponível.');
  pyodide.runPython(await response.text());
  // JSON só transporta os dados. O algoritmo está no arquivo cod-mult-matriz.py.
  pyodide.runPython(`
import json

def _resolver_json(entrada_json):
    try:
        entrada = json.loads(entrada_json)
        resultado = multiplicar_matrizes(entrada["a"], entrada["b"])
        return json.dumps({"ok": True, "dados": resultado}, allow_nan=False)
    except ValueError as erro:
        return json.dumps({"ok": False, "erro": str(erro)})
`);
  const resolver = pyodide.globals.get('_resolver_json');
  self.postMessage({type: 'ready'});
  return resolver;
})();

ready.catch(() => self.postMessage({type: 'init-error'}));
self.onmessage = async ({data}) => {
  try {
    const resolver = await ready;
    self.postMessage({id: data.id, ...JSON.parse(resolver(data.json))});
  } catch {
    self.postMessage({id: data.id, ok: false, erro: 'Não foi possível executar o Python. Atualize a página para tentar novamente.'});
  }
};
