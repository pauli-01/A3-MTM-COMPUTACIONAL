"""MatrizLab A3 — Multiplicação de matrizes em Python."""


def contar(itens):
    """Conta os elementos de uma sequência com um laço."""
    quantidade = 0
    for item in itens:
        quantidade += 1
    return quantidade


def validar_matriz(matriz):
    """Retorna as dimensões e uma mensagem se a matriz for inválida."""
    try:
        linhas = contar(matriz)
        if linhas < 1 or linhas > 6:
            return None, "A matriz precisa ter de 1 a 6 linhas."

        colunas = contar(matriz[0])
        if colunas < 1 or colunas > 6:
            return None, "A matriz precisa ter de 1 a 6 colunas."

        for linha in matriz:
            if contar(linha) != colunas:
                return None, "Todas as linhas precisam ter o mesmo tamanho."
            for valor in linha:
                if valor is True or valor is False:
                    return None, "Preencha a matriz com valores numéricos."
                if not -1_000_000_000_000 <= valor <= 1_000_000_000_000:
                    return None, "Use valores entre -1 trilhão e 1 trilhão."
    except (TypeError, IndexError, KeyError):
        return None, "Use uma lista de linhas preenchidas com números."

    return [linhas, colunas], None


def multiplicar_matrizes(a, b):
    """Calcula C = A × B e guarda a conta de cada posição."""
    dimensoes_a, erro_a = validar_matriz(a)
    if erro_a:
        return {"erro": "Matriz A. " + erro_a}

    dimensoes_b, erro_b = validar_matriz(b)
    if erro_b:
        return {"erro": "Matriz B. " + erro_b}

    linhas_a, colunas_a = dimensoes_a
    linhas_b, colunas_b = dimensoes_b
    if colunas_a != linhas_b:
        return {"erro": "O número de colunas de A deve ser igual ao de linhas de B."}

    resultado = []
    passos = []
    i = 0
    while i < linhas_a:
        linha_c = []
        j = 0
        while j < colunas_b:
            total = 0
            termos = []
            k = 0

            while k < colunas_a:
                valor_a = a[i][k]
                valor_b = b[k][j]
                produto = valor_a * valor_b
                total += produto
                termos += [{
                    "a": valor_a,
                    "b": valor_b,
                    "produto": produto,
                    "acumulado": total,
                }]
                k += 1

            linha_c += [total]
            passos += [{
                "linha": i + 1,
                "coluna": j + 1,
                "termos": termos,
                "valor": total,
            }]
            j += 1

        resultado += [linha_c]
        i += 1

    return {
        "resultado": resultado,
        "passos": passos,
        "dimensoes": {"a": dimensoes_a, "b": dimensoes_b, "c": [linhas_a, colunas_b]},
    }


A = [[1, 2, 3], [4, 5, 6]]
B = [[7, 8], [9, 10], [11, 12]]
exemplo = multiplicar_matrizes(A, B)
