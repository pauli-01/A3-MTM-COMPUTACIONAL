"""Servidor HTTP local para a interface de multiplicação."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from calculo import formatar_numero, multiplicar_matrizes


PASTA_PROJETO = Path(__file__).resolve().parent
ENDERECO = "127.0.0.1"
PORTA = 8000
LIMITE_REQUISICAO = 16_384  # bytes

# Só estes arquivos são publicados pelo servidor.
ARQUIVOS = {
    "/": ("site/index.html", "text/html"),
    "/estilo.css": ("site/estilo.css", "text/css"),
    "/interface.js": ("site/interface.js", "text/javascript"),
    "/apresentacao/": ("apresentacao/index.html", "text/html"),
    "/apresentacao/estilo.css": ("apresentacao/estilo.css", "text/css"),
    "/apresentacao/apresentacao.js": (
        "apresentacao/apresentacao.js", "text/javascript"
    ),
}


def resposta_json(status, dados):
    conteudo = json.dumps(dados, ensure_ascii=False, allow_nan=False)
    return status, "application/json", conteudo.encode("utf-8")


def servir_arquivo(rota):
    if rota not in ARQUIVOS:
        return resposta_json(404, {"erro": "Página não encontrada."})

    caminho, tipo = ARQUIVOS[rota]
    try:
        conteudo = (PASTA_PROJETO / caminho).read_bytes()
    except OSError:
        return resposta_json(500, {"erro": "Não foi possível abrir o arquivo."})
    return 200, tipo, conteudo


def responder_calculo(rota, tipo, tamanho, ler_corpo):
    if rota != "/api/calcular":
        return resposta_json(404, {"erro": "Endereço de cálculo não encontrado."})
    if tipo != "application/json":
        return resposta_json(415, {"erro": "Envie os dados no formato JSON."})

    # Confere o tamanho antes de ler qualquer dado da requisição.
    try:
        tamanho = int(tamanho)
    except (ValueError, TypeError):
        tamanho = 0
    if tamanho <= 0:
        return resposta_json(400, {"erro": "Tamanho da requisição inválido."})
    if tamanho > LIMITE_REQUISICAO:
        return resposta_json(413, {"erro": "Requisição muito grande."})

    try:
        corpo = ler_corpo(tamanho)
        if len(corpo) != tamanho:
            raise ValueError("Corpo incompleto")
        dados = json.loads(corpo.decode("utf-8"))
    except (ValueError, RecursionError):
        return resposta_json(400, {"erro": "O conteúdo enviado não é um JSON válido."})
    if not isinstance(dados, dict) or dados.keys() != {"a", "b"}:
        return resposta_json(400, {"erro": "Envie as matrizes A e B."})

    try:
        resultado, passos = multiplicar_matrizes(dados["a"], dados["b"])
    except ValueError as erro:
        return resposta_json(400, {"erro": str(erro)})

    # Preserva no navegador os dígitos exibidos pelo Python.
    resultado_formatado = []
    for linha in resultado:
        linha_formatada = []
        for valor in linha:
            linha_formatada.append(formatar_numero(valor))
        resultado_formatado.append(linha_formatada)

    return resposta_json(200, {
        "resultado": resultado,
        "resultado_formatado": resultado_formatado,
        "passos": passos,
    })


class ServidorMatrizes(BaseHTTPRequestHandler):
    """Recebe as requisições do navegador no modo local."""

    def responder(self, status, tipo, conteudo):
        self.send_response(status)
        self.send_header("Content-Type", f"{tipo}; charset=utf-8")
        self.send_header("Content-Length", str(len(conteudo)))
        self.end_headers()
        self.wfile.write(conteudo)

    def do_GET(self):
        rota = self.path.partition("?")[0]
        self.responder(*servir_arquivo(rota))

    def do_POST(self):
        tamanhos = self.headers.get_all("Content-Length", [])
        tamanho = None
        if len(tamanhos) == 1 and not self.headers.get("Transfer-Encoding"):
            tamanho = tamanhos[0]
        self.responder(*responder_calculo(
            self.path, self.headers.get_content_type(), tamanho, self.rfile.read
        ))


def criar_servidor(porta=PORTA):
    """Restringe a escuta ao computador em que o programa é executado."""
    return ThreadingHTTPServer((ENDERECO, porta), ServidorMatrizes)


def principal():
    try:
        servidor = criar_servidor()
    except OSError:
        print(f"Não foi possível iniciar o servidor na porta {PORTA}.")
        print("Verifique se outro programa já está usando essa porta.")
        return 1

    with servidor:
        print(f"Abra http://{ENDERECO}:{PORTA} no navegador.")
        print("Pressione Ctrl+C para encerrar.")
        try:
            servidor.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
