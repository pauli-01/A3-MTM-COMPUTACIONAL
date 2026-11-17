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


class ServidorMatrizes(BaseHTTPRequestHandler):
    """Recebe as requisições do navegador e envia as respostas HTTP."""

    def responder(self, status, tipo, conteudo):
        self.send_response(status)
        self.send_header("Content-Type", f"{tipo}; charset=utf-8")
        self.send_header("Content-Length", str(len(conteudo)))
        self.end_headers()
        self.wfile.write(conteudo)

    def responder_json(self, status, dados):
        conteudo = json.dumps(dados, ensure_ascii=False, allow_nan=False)
        self.responder(status, "application/json", conteudo.encode("utf-8"))

    def do_GET(self):
        rota = self.path.partition("?")[0]
        if rota not in ARQUIVOS:
            self.responder_json(404, {"erro": "Página não encontrada."})
            return

        caminho, tipo = ARQUIVOS[rota]
        try:
            conteudo = (PASTA_PROJETO / caminho).read_bytes()
        except OSError:
            self.responder_json(500, {"erro": "Não foi possível abrir o arquivo."})
            return
        self.responder(200, tipo, conteudo)

    def do_POST(self):
        if self.path != "/api/calcular":
            self.responder_json(404, {"erro": "Endereço de cálculo não encontrado."})
            return
        if self.headers.get_content_type() != "application/json":
            self.responder_json(415, {"erro": "Envie os dados no formato JSON."})
            return

        # Limita o corpo antes da leitura e retorna erros em linguagem simples.
        tamanhos = self.headers.get_all("Content-Length", [])
        if len(tamanhos) != 1 or self.headers.get("Transfer-Encoding"):
            self.responder_json(400, {"erro": "Tamanho da requisição inválido."})
            return
        try:
            tamanho = int(tamanhos[0])
        except ValueError:
            tamanho = 0
        if tamanho <= 0:
            self.responder_json(400, {"erro": "Tamanho da requisição inválido."})
            return
        if tamanho > LIMITE_REQUISICAO:
            self.responder_json(413, {"erro": "Requisição muito grande."})
            return

        try:
            corpo = self.rfile.read(tamanho)
            if len(corpo) != tamanho:
                raise ValueError("Corpo incompleto")
            dados = json.loads(corpo.decode("utf-8"))
        except (ValueError, RecursionError):
            self.responder_json(400, {"erro": "O conteúdo enviado não é um JSON válido."})
            return
        if not isinstance(dados, dict) or dados.keys() != {"a", "b"}:
            self.responder_json(400, {"erro": "Envie as matrizes A e B."})
            return

        try:
            resultado, passos = multiplicar_matrizes(dados["a"], dados["b"])
        except ValueError as erro:
            self.responder_json(400, {"erro": str(erro)})
            return

        # Preserva no navegador os dígitos exibidos pelo Python.
        resultado_formatado = []
        for linha in resultado:
            linha_formatada = []
            for valor in linha:
                linha_formatada.append(formatar_numero(valor))
            resultado_formatado.append(linha_formatada)

        self.responder_json(200, {
            "resultado": resultado,
            "resultado_formatado": resultado_formatado,
            "passos": passos,
        })


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
