"""MatrizLab A3 — Multiplicação de matrizes em Python."""


def contar(itens):
    # Somo 1 para cada item que encontro na lista.
    total = 0
    for item in itens:
        total += 1
    return total


def validar_matriz(matriz):
    limite = 1_000_000_000_000

    try:
        linhas = contar(matriz)
        if linhas < 1 or linhas > 6:
            return None, "A matriz precisa ter de 1 a 6 linhas."

        # A primeira linha serve de referência para as outras.
        colunas = contar(matriz[0])
        if colunas < 1 or colunas > 6:
            return None, "A matriz precisa ter de 1 a 6 colunas."

        for linha in matriz:
            tamanho_da_linha = contar(linha)
            if tamanho_da_linha != colunas:
                return None, "Todas as linhas precisam ter o mesmo tamanho."

            for numero in linha:
                if numero is True or numero is False:
                    return None, "Preencha a matriz com valores numéricos."
                if not (-limite <= numero <= limite):
                    return None, "Use valores entre -1 trilhão e 1 trilhão."
    except (TypeError, IndexError, KeyError):
        return None, "Use uma lista de linhas preenchidas com números."

    return [linhas, colunas], None


def multiplicar_matrizes(a, b):
    dimensoes_a, erro = validar_matriz(a)
    if erro:
        return {"erro": "Matriz A. " + erro}

    dimensoes_b, erro = validar_matriz(b)
    if erro:
        return {"erro": "Matriz B. " + erro}

    linhas_a, colunas_a = dimensoes_a
    linhas_b, colunas_b = dimensoes_b
    if colunas_a != linhas_b:
        return {"erro": "O número de colunas de A deve ser igual ao de linhas de B."}

    resultado = []
    passos = []

    # i é a linha de A que estou usando.
    i = 0
    while i < linhas_a:
        linha_a = a[i]
        linha_resultado = []

        # j é a coluna de B que estou usando.
        j = 0
        while j < colunas_b:
            # Cada posição de C começa com uma soma nova.
            soma = 0
            termos = []

            # k anda na linha de A e na coluna de B ao mesmo tempo.
            k = 0
            while k < colunas_a:
                valor_a = linha_a[k]
                valor_b = b[k][j]
                produto = valor_a * valor_b
                soma += produto

                conta_do_par = {
                    "a": valor_a,
                    "b": valor_b,
                    "produto": produto,
                    "acumulado": soma,
                }
                termos += [conta_do_par]
                k += 1

            # Guardo a soma na matriz e a conta para mostrar no site.
            linha_resultado += [soma]
            conta_da_posicao = {
                "linha": i + 1,
                "coluna": j + 1,
                "termos": termos,
                "valor": soma,
            }
            passos += [conta_da_posicao]
            j += 1

        resultado += [linha_resultado]
        i += 1

    return {
        "resultado": resultado,
        "passos": passos,
        "dimensoes": {"a": dimensoes_a, "b": dimensoes_b, "c": [linhas_a, colunas_b]},
    }


A = [[1, 2, 3], [4, 5, 6]]
B = [[7, 8], [9, 10], [11, 12]]
exemplo = multiplicar_matrizes(A, B)
