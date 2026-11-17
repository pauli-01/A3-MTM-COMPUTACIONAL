import json
import unittest
from io import BytesIO
from wsgiref.util import setup_testing_defaults
from wsgiref.validate import validator

from hospedagem import aplicacao


class TesteHospedagem(unittest.TestCase):
    def requisicao(self, metodo, rota, corpo=b"", tipo="application/json"):
        # Simula o ambiente que um servidor WSGI entrega à aplicação.
        ambiente = {
            "REQUEST_METHOD": metodo,
            "SCRIPT_NAME": "",
            "PATH_INFO": rota,
            "QUERY_STRING": "",
            "CONTENT_TYPE": tipo,
            "CONTENT_LENGTH": str(len(corpo)),
            "wsgi.input": BytesIO(corpo),
        }
        setup_testing_defaults(ambiente)

        resposta = {}
        blocos = []

        def iniciar_resposta(status, cabecalhos, exc_info=None):
            resposta["status"] = int(status.split()[0])
            resposta["cabecalhos"] = dict(cabecalhos)
            return blocos.append

        # O validador também verifica o contrato WSGI enquanto lê a resposta.
        conteudo = validator(aplicacao)(ambiente, iniciar_resposta)
        try:
            blocos.extend(conteudo)
        finally:
            conteudo.close()
        return resposta["status"], resposta["cabecalhos"], b"".join(blocos)

    def verificar_erro(self, status_esperado, metodo, rota, corpo=b"", tipo="application/json"):
        status, cabecalhos, resposta = self.requisicao(metodo, rota, corpo, tipo)
        self.assertEqual(status, status_esperado)
        self.assertIn("application/json", cabecalhos["Content-Type"])
        mensagem = json.loads(resposta)["erro"]
        self.assertIsInstance(mensagem, str)
        self.assertTrue(mensagem.strip())
        self.assertNotIn("Traceback", mensagem)

    def test_entrega_pagina_principal(self):
        status, cabecalhos, resposta = self.requisicao("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn("text/html", cabecalhos["Content-Type"])
        self.assertIn("Multiplicação de Matrizes", resposta.decode("utf-8"))

    def test_calcula_exemplo_e_entrega_passos(self):
        dados = {"a": [[1, 2, 3], [4, 5, 6]], "b": [[7, 8], [9, 10], [11, 12]]}
        corpo = json.dumps(dados).encode("utf-8")
        status, cabecalhos, resposta = self.requisicao("POST", "/api/calcular", corpo)
        self.assertEqual(status, 200)
        self.assertIn("application/json", cabecalhos["Content-Type"])
        dados = json.loads(resposta)
        self.assertEqual(dados["resultado"], [[58, 64], [139, 154]])
        self.assertEqual(dados["resultado_formatado"], [["58", "64"], ["139", "154"]])
        self.assertEqual(dados["passos"][0][0], "C[1,1] = (1 × 7) + (2 × 9) + (3 × 11) = 58")

    def test_rejeita_tipo_de_conteudo_invalido(self):
        self.verificar_erro(415, "POST", "/api/calcular", b"matrizes", "text/plain")

    def test_rejeita_json_invalido(self):
        for corpo in (b"{", b"\xff", b'{"a": [[1]]}'):
            with self.subTest(corpo=corpo):
                self.verificar_erro(400, "POST", "/api/calcular", corpo)

    def test_rejeita_rota_inexistente(self):
        self.verificar_erro(404, "GET", "/nao-existe")


if __name__ == "__main__":
    unittest.main()
