const matrizes = [
    {
        nome: "A",
        linhas: document.querySelector("#linhas-a"),
        colunas: document.querySelector("#colunas-a"),
        grade: document.querySelector("#grade-a"),
        dimensao: document.querySelector("#dimensao-a"),
        exemplo: [[1, 2, 3], [4, 5, 6]]
    },
    {
        nome: "B",
        linhas: document.querySelector("#linhas-b"),
        colunas: document.querySelector("#colunas-b"),
        grade: document.querySelector("#grade-b"),
        dimensao: document.querySelector("#dimensao-b"),
        exemplo: [[7, 8], [9, 10], [11, 12]]
    }
];

const formulario = document.querySelector("#formulario");
const calcular = document.querySelector("#calcular");
const compatibilidade = document.querySelector("#compatibilidade");
const erro = document.querySelector("#erro");
const resultado = document.querySelector("#resultado");
const dimensaoC = document.querySelector("#dimensao-c");
const situacao = document.querySelector("#situacao");
const tabelaC = document.querySelector("#valores-c");
const listaPassos = document.querySelector("#passos");
const dica = "O resultado e o passo a passo aparecem aqui após o cálculo.";
const numeroDecimal = /^[+-]?(?:[0-9]+(?:[.,][0-9]*)?|[.,][0-9]+)$/;
let pedido = null;

// Gera as opções e a grade, preservando as células que ainda cabem ao redimensionar.
function preencherOpcoes(campo) {
    for (let tamanho = 1; tamanho <= 6; tamanho++) {
        campo.add(new Option(tamanho, tamanho));
    }
}

function montarGrade(matriz, valores) {
    const linhas = Number(matriz.linhas.value);
    const colunas = Number(matriz.colunas.value);
    matriz.dimensao.textContent = linhas + " × " + colunas;
    matriz.grade.replaceChildren();

    for (let i = 0; i < linhas; i++) {
        const linha = document.createElement("div");
        linha.className = "linha-matriz";
        for (let j = 0; j < colunas; j++) {
            const campo = document.createElement("input");
            campo.type = "text";
            campo.inputMode = "decimal";
            campo.autocomplete = "off";
            campo.setAttribute("aria-describedby", "dica-valores");
            campo.setAttribute("aria-label", "Matriz " + matriz.nome + ", linha " + (i + 1) + ", coluna " + (j + 1));
            campo.value = valores[i]?.[j] ?? "";
            linha.append(campo);
        }
        matriz.grade.append(linha);
    }
}

function atualizarCompatibilidade() {
    const colunasA = matrizes[0].colunas.value;
    const linhasB = matrizes[1].linhas.value;
    const compativel = colunasA === linhasB;
    compatibilidade.classList.toggle("incompativel", !compativel);
    if (compativel) {
        compatibilidade.textContent = "Dimensões compatíveis · " + colunasA +
            (colunasA === "1" ? " coluna em A e 1 linha em B." : " colunas em A e " + linhasB + " linhas em B.");
    } else {
        compatibilidade.textContent = "Dimensões incompatíveis. Iguale as colunas de A às linhas de B.";
    }
    return compativel;
}

function limparErro() {
    const campo = formulario.querySelector('[aria-invalid="true"]');
    if (campo) {
        campo.removeAttribute("aria-invalid");
        campo.removeAttribute("aria-errormessage");
    }
    erro.hidden = true;
    erro.textContent = "";
}

function mostrarErro(mensagem, campo) {
    erro.textContent = mensagem;
    erro.hidden = false;
    if (campo) {
        campo.setAttribute("aria-invalid", "true");
        campo.setAttribute("aria-errormessage", "erro");
        campo.focus();
    }
}

function limparResultado(mensagem) {
    if (pedido) {
        pedido.abort();
        pedido = null;
    }
    calcular.disabled = false;
    calcular.textContent = "Calcular";
    resultado.hidden = true;
    dimensaoC.hidden = true;
    situacao.textContent = mensagem;
}

function usarDimensoesDoExemplo(preencher) {
    for (const matriz of matrizes) {
        matriz.linhas.value = matriz.exemplo.length;
        matriz.colunas.value = matriz.exemplo[0].length;
        montarGrade(matriz, preencher ? matriz.exemplo : []);
    }
    atualizarCompatibilidade();
}

for (const matriz of matrizes) {
    for (const seletor of [matriz.linhas, matriz.colunas]) {
        preencherOpcoes(seletor);
        seletor.addEventListener("change", () => {
            const valores = [];
            for (const linha of matriz.grade.children) {
                valores.push(Array.from(linha.children, campo => campo.value));
            }
            montarGrade(matriz, valores);
            limparErro();
            limparResultado(dica);
            atualizarCompatibilidade();
        });
    }
}

usarDimensoesDoExemplo(false);
formulario.addEventListener("input", () => {
    limparErro();
    limparResultado(dica);
});

document.querySelector("#exemplo").addEventListener("click", () => {
    limparErro();
    usarDimensoesDoExemplo(true);
    limparResultado("Exemplo preenchido. Selecione Calcular para ver o resultado.");
});

document.querySelector("#limpar").addEventListener("click", () => {
    limparErro();
    for (const matriz of matrizes) {
        montarGrade(matriz, []);
    }
    limparResultado("Valores apagados. Preencha as duas matrizes para calcular novamente.");
});

// Confere os campos e mantém os decimais como texto para o Python interpretar.
function lerMatriz(matriz) {
    const valores = [];
    for (const linha of matriz.grade.children) {
        const numeros = [];
        for (const campo of linha.children) {
            const valor = campo.value.trim();
            const posicao = campo.getAttribute("aria-label");
            if (valor === "") {
                mostrarErro(posicao + ". Preencha este campo.", campo);
                return null;
            }
            if (!numeroDecimal.test(valor)) {
                mostrarErro(posicao + ". Digite um número com vírgula ou ponto para decimais.", campo);
                return null;
            }
            numeros.push(valor);
        }
        valores.push(numeros);
    }
    return valores;
}

// Mostra o resultado e as contas que o servidor produziu.
function exibirResultado(dados) {
    tabelaC.replaceChildren();
    listaPassos.replaceChildren();

    for (const linha of dados.resultado_formatado) {
        const linhaC = tabelaC.insertRow();
        for (const valor of linha) {
            linhaC.insertCell().textContent = valor;
        }
    }

    for (const linha of dados.passos) {
        for (const conta of linha) {
            const item = document.createElement("li");
            item.textContent = conta;
            listaPassos.append(item);
        }
    }

    dimensaoC.textContent = dados.resultado_formatado.length + " × " + dados.resultado_formatado[0].length;
    dimensaoC.hidden = false;
    situacao.textContent = "Resultado calculado.";
    resultado.hidden = false;
    document.querySelector("#titulo-c").focus();
}

formulario.addEventListener("submit", async evento => {
    evento.preventDefault();
    limparErro();
    limparResultado(dica);

    if (!atualizarCompatibilidade()) {
        mostrarErro("Para calcular, iguale as colunas de A às linhas de B.", matrizes[1].linhas);
        return;
    }

    const a = lerMatriz(matrizes[0]);
    if (a === null) {
        return;
    }

    const b = lerMatriz(matrizes[1]);
    if (b === null) {
        return;
    }

    // Cancela uma solicitação antiga se o usuário editar os dados.
    const envio = new AbortController();
    pedido = envio;
    calcular.disabled = true;
    calcular.textContent = "Calculando…";
    situacao.textContent = "Calculando…";

    try {
        const resposta = await fetch("/api/calcular", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ a, b }),
            signal: envio.signal
        });
        const dados = await resposta.json();

        if (pedido !== envio) {
            return;
        }

        if (resposta.ok) {
            exibirResultado(dados);
        } else {
            situacao.textContent = dica;
            mostrarErro(dados.erro);
        }
    } catch {
        if (pedido === envio) {
            situacao.textContent = dica;
            mostrarErro("Não foi possível receber o cálculo. Confira se o servidor Python está em execução.");
        }
    } finally {
        if (pedido === envio) {
            pedido = null;
            calcular.disabled = false;
            calcular.textContent = "Calcular";
        }
    }
});
