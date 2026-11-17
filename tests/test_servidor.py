import json
import unittest
from http.client import HTTPConnection
from threading import Thread

from servidor import LIMITE_REQUISICAO, criar_servidor


class TesteServidor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Porta 0 pede ao sistema uma porta livre, sem interferir no site aberto.
        cls.servidor = criar_servidor(porta=0)
        cls.addClassCleanup(cls.servidor.server_close)
        cls.execucao = Thread(target=cls.servidor.serve_forever, daemon=True)
        cls.execucao.start()
        cls.addClassCleanup(cls.encerrar_execucao)

    @classmethod
    def encerrar_execucao(cls):
        cls.servidor.shutdown()
        cls.execucao.join(timeout=5)

    def requisicao(self, metodo, caminho, corpo=None, tipo="application/json"):
        endereco, porta = self.servidor.server_address
        self.assertEqual(endereco, "127.0.0.1")
        conexao = HTTPConnection(endereco, porta, timeout=5)
        try:
            conexao.request(metodo, caminho, corpo, {"Content-Type": tipo})
            resposta = conexao.getresponse()
            return resposta.status, resposta.getheader("Content-Type", ""), resposta.read()
        finally:
            conexao.close()

    def verificar_erro(self, corpo, tipo="application/json", status_esperado=400):
        status, tipo_resposta, resposta = self.requisicao("POST", "/api/calcular", corpo, tipo)
        self.assertEqual(status, status_esperado, resposta)
        self.assertIn("application/json", tipo_resposta)
        mensagem = json.loads(resposta)["erro"]
        self.assertIsInstance(mensagem, str)
        self.assertTrue(mensagem.strip())
        self.assertNotIn("Traceback", mensagem)

    def test_entrega_arquivos_da_interface(self):
        arquivos = (
            ("/", "text/html", "Multiplicação de Matrizes"),
            ("/estilo.css", "text/css", None),
            ("/interface.js", "javascript", "/api/calcular"),
            ("/apresentacao/", "text/html", "Multiplicação de Matrizes | Apresentação"),
            ("/apresentacao/estilo.css", "text/css", "@media print"),
            ("/apresentacao/apresentacao.js", "javascript", None),
        )
        for caminho, mime, trecho in arquivos:
            with self.subTest(caminho=caminho):
                status, tipo, corpo = self.requisicao("GET", caminho)
                self.assertEqual(status, 200)
                self.assertIn(mime, tipo)
                self.assertTrue(corpo.strip())
                if trecho is not None:
                    self.assertIn(trecho, corpo.decode("utf-8"))

    def test_api_calcula_exemplo_e_envia_detalhamento(self):
        dados = {"a": [[1, 2, 3], [4, 5, 6]], "b": [[7, 8], [9, 10], [11, 12]]}
        status, tipo, corpo = self.requisicao("POST", "/api/calcular", json.dumps(dados))
        self.assertEqual(status, 200)
        self.assertIn("application/json", tipo)
        dados = json.loads(corpo)
        self.assertEqual(dados["resultado"], [[58, 64], [139, 154]])
        self.assertEqual(dados["passos"][0][0], "C[1,1] = (1 × 7) + (2 × 9) + (3 × 11) = 58")

    def test_api_aceita_decimais_em_texto(self):
        dados = {"a": [["-2,5", "3.1"]], "b": [["4"], ["2"]]}
        status, _, resposta = self.requisicao("POST", "/api/calcular", json.dumps(dados))
        self.assertEqual(status, 200)
        dados = json.loads(resposta)
        self.assertAlmostEqual(dados["resultado"][0][0], -3.8, delta=1e-9)
        self.assertEqual(dados["resultado_formatado"], [["-3,8"]])

    def test_api_rejeita_json_malformado(self):
        for corpo in (b"{", b"\xff", b"", b'"matrizes"', b'{"a": [[1]]}'):
            with self.subTest(corpo=corpo):
                self.verificar_erro(corpo)

    def test_api_rejeita_tipo_de_conteudo_invalido(self):
        self.verificar_erro(b"a=1&b=2", tipo="text/plain", status_esperado=415)

    def test_api_rejeita_corpo_acima_do_limite(self):
        self.verificar_erro(b" " * (LIMITE_REQUISICAO + 1), status_esperado=413)

    def test_api_rejeita_matrizes_invalidas(self):
        casos = (
            {"a": [[1, 2]], "b": [[3]]},
            {"a": [[1, 2], [3]], "b": [[4], [5]]},
            {"a": [[""]], "b": [[1]]},
            {"a": [[1]] * 7, "b": [[1]]},
            {"a": [[float("inf")]], "b": [[1]]},
        )
        for dados in casos:
            with self.subTest(dados=dados):
                self.verificar_erro(json.dumps(dados))


if __name__ == "__main__":
    unittest.main()
