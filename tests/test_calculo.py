import subprocess
import sys
import unittest
from pathlib import Path

import calculo
import terminal


class TesteCalculo(unittest.TestCase):
    def verificar_produto(self, matriz_a, matriz_b, esperado):
        # Executa o mesmo caso nas duas implementações independentes.
        resultado_web, _ = calculo.multiplicar_matrizes(matriz_a, matriz_b)
        resultado_terminal = terminal.multiplicar_matrizes(matriz_a, matriz_b)
        for nome, resultado in (("site", resultado_web), ("terminal", resultado_terminal)):
            with self.subTest(implementacao=nome):
                self.assertEqual(len(resultado), len(esperado))
                for linha, linha_esperada in zip(resultado, esperado):
                    self.assertEqual(len(linha), len(linha_esperada))
                    for valor, valor_esperado in zip(linha, linha_esperada):
                        self.assertAlmostEqual(valor, valor_esperado, delta=1e-9)

    def verificar_entrada_invalida(self, matriz_a, matriz_b):
        for modulo in (calculo, terminal):
            with self.subTest(implementacao=modulo.__name__):
                with self.assertRaises(ValueError):
                    modulo.multiplicar_matrizes(matriz_a, matriz_b)

    def test_exemplo_obrigatorio(self):
        matriz_a = [[1, 2, 3], [4, 5, 6]]
        matriz_b = [[7, 8], [9, 10], [11, 12]]
        self.verificar_produto(matriz_a, matriz_b, [[58, 64], [139, 154]])

    def test_detalhamento_dos_quatro_elementos(self):
        matriz_a = [[1, 2, 3], [4, 5, 6]]
        matriz_b = [[7, 8], [9, 10], [11, 12]]
        _, passos = calculo.multiplicar_matrizes(matriz_a, matriz_b)
        self.assertEqual(
            passos,
            [
                [
                    "C[1,1] = (1 × 7) + (2 × 9) + (3 × 11) = 58",
                    "C[1,2] = (1 × 8) + (2 × 10) + (3 × 12) = 64",
                ],
                [
                    "C[2,1] = (4 × 7) + (5 × 9) + (6 × 11) = 139",
                    "C[2,2] = (4 × 8) + (5 × 10) + (6 × 12) = 154",
                ],
            ],
        )

    def test_identidade(self):
        matriz = [[2, 3], [4, -5], [0, 1]]
        identidade = [[1, 0], [0, 1]]
        self.verificar_produto(matriz, identidade, matriz)

    def test_matriz_zero(self):
        self.verificar_produto([[1, 2], [3, 4]], [[0], [0]], [[0], [0]])

    def test_retangulares_com_resultado_de_tamanho_distinto(self):
        self.verificar_produto([[2], [-3]], [[4, 5, 0]], [[8, 10, 0], [-12, -15, 0]])

    def test_um_por_um(self):
        self.verificar_produto([[7]], [[-3]], [[-21]])

    def test_negativos_e_decimais_com_virgula_e_ponto(self):
        self.verificar_produto([["-0,1", "0.2"]], [[3], [1.5]], [[0]])
        self.verificar_produto([["2,5", "-1.2"]], [[4], [0.5]], [[9.4]])

    def test_dimensoes_incompativeis(self):
        self.verificar_entrada_invalida([[1, 2]], [[3, 4]])

    def test_estruturas_invalidas(self):
        for matriz in ([], [[]], [1, 2], [[1], [2, 3]], None, {"linha": [1]}):
            with self.subTest(matriz=matriz):
                self.verificar_entrada_invalida(matriz, [[1]])
                self.verificar_entrada_invalida([[1]], matriz)

    def test_limite_de_seis_linhas_ou_colunas(self):
        self.verificar_produto([[1, 2, 3, 4, 5, 6]], [[1], [1], [1], [1], [1], [1]], [[21]])
        self.verificar_entrada_invalida([[1]] * 7, [[1]])
        self.verificar_entrada_invalida([[1]], [[1] * 7])

    def test_elementos_invalidos(self):
        invalidos = (
            "", "   ", "texto", "1.234,56", "1 234", None, True, [],
            "NaN", "Infinity", float("nan"), float("inf"), float("-inf"),
        )
        for valor in invalidos:
            with self.subTest(valor=valor):
                self.verificar_entrada_invalida([[valor]], [[1]])
                self.verificar_entrada_invalida([[1]], [[valor]])

    def test_produto_fora_da_faixa_numerica(self):
        self.verificar_entrada_invalida([[1e308]], [[10]])


class TesteTerminal(unittest.TestCase):
    def executar_terminal(self, dados):
        pasta_projeto = Path(__file__).resolve().parents[1]
        processo = subprocess.run(
            [sys.executable, "-X", "utf8", str(pasta_projeto / "terminal.py")],
            input=dados,
            encoding="utf-8",
            capture_output=True,
            timeout=10,
        )
        self.assertEqual(processo.returncode, 0, processo.stderr)
        return processo.stdout

    def test_executa_o_exemplo_no_terminal(self):
        # Dimensões de A e B, elementos em ordem de leitura e resposta para sair.
        dados = "2\n3\n3\n2\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\nn\n"
        saida = self.executar_terminal(dados)
        self.assertIn("Matriz A (2 × 3)", saida)
        self.assertIn("Matriz B (3 × 2)", saida)
        self.assertIn("Matriz C (2 × 2)", saida)
        self.assertRegex(saida, r"\[\s*58\s+64\s*\]")
        self.assertRegex(saida, r"\[\s*139\s+154\s*\]")

    def test_corrige_entradas_e_repete_calculo(self):
        dados = (
            "0\n1\n2\n1\n1\ns\n"  # Dimensão zero, depois A 1 × 2 e B 1 × 1.
            "1\n1\n1\n1\ntexto\n2,5\n-3\ns\n"  # Corrige a célula de A e calcula.
            "1\n1\n1\n1\n2\n4\nn\n"  # Repete e encerra.
        )
        saida = self.executar_terminal(dados)
        self.assertIn("Digite um inteiro", saida)
        self.assertIn("Dimensões incompatíveis", saida)
        self.assertIn("Digite um número", saida)
        self.assertEqual(saida.count("Matriz C (1 × 1)"), 2)
        self.assertRegex(saida, r"\[\s*-7,5\s*\]")
        self.assertRegex(saida, r"\[\s*8\s*\]")


if __name__ == "__main__":
    unittest.main()
