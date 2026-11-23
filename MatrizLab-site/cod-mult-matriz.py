"""Multiplicação de matrizes — núcleo matemático, sem importar bibliotecas."""


def formatar_numero(numero):
    """Prepara um número para a tela, com até 12 algarismos significativos."""
    if numero == int(numero):
        return str(int(numero))
    return format(numero, ".12g").replace(".", ",")


def ler_numero(valor, nome, linha, coluna):
    """Aceita números decimais com vírgula ou ponto e rejeita dados inválidos."""
    local = f"Matriz {nome}, linha {linha + 1}, coluna {coluna + 1}"
    if isinstance(valor, bool) or not isinstance(valor, (str, int, float)):
        raise ValueError(f"{local}: digite um número válido.")
    if isinstance(valor, str):
        texto = valor.strip().replace(",", ".")
        if not texto:
            raise ValueError(f"{local}: preencha este campo.")
        if texto[0] in "+-":
            texto = texto[1:]
        pontos = 0
        digitos = 0
        for caractere in texto:
            if caractere == ".":
                pontos += 1
            elif caractere in "0123456789":
                digitos += 1
            else:
                raise ValueError(f"{local}: use números, com vírgula ou ponto decimal.")
        if pontos > 1 or digitos == 0:
            raise ValueError(f"{local}: digite um número válido.")
    try:
        numero = float(str(valor).strip().replace(",", "."))
    except (ValueError, OverflowError):
        raise ValueError(f"{local}: digite um número válido.") from None
    # O limite mantém o demonstrador legível e evita valores infinitos.
    if numero != numero or numero < -1_000_000_000_000 or numero > 1_000_000_000_000:
        raise ValueError(f"{local}: use um número entre −1 trilhão e 1 trilhão.")
    return numero


def validar_matriz(matriz, nome):
    """Confere tamanho, formato retangular e valores de uma matriz."""
    if not isinstance(matriz, list) or not 1 <= len(matriz) <= 6:
        raise ValueError(f"A matriz {nome} deve ter de 1 a 6 linhas.")
    if not isinstance(matriz[0], list) or not 1 <= len(matriz[0]) <= 6:
        raise ValueError(f"A matriz {nome} deve ter de 1 a 6 colunas.")
    colunas = len(matriz[0])
    validada = []
    for i in range(len(matriz)):
        if not isinstance(matriz[i], list) or len(matriz[i]) != colunas:
            raise ValueError(f"Todas as linhas da matriz {nome} devem ter o mesmo tamanho.")
        linha = []
        for j in range(colunas):
            linha.append(ler_numero(matriz[i][j], nome, i, j))
        validada.append(linha)
    return validada


def multiplicar_matrizes(matriz_a, matriz_b):
    """Calcula A × B e registra a explicação de cada elemento do resultado."""
    a = validar_matriz(matriz_a, "A")
    b = validar_matriz(matriz_b, "B")
    linhas_a = len(a)
    colunas_a = len(a[0])
    linhas_b = len(b)
    colunas_b = len(b[0])

    # A multiplicação só existe quando colunas de A = linhas de B.
    if colunas_a != linhas_b:
        raise ValueError(
            f"Não é possível multiplicar: A tem {colunas_a} coluna(s), "
            f"mas B tem {linhas_b} linha(s). Esses números precisam ser iguais."
        )

    resultado = []
    passos = []
    # i escolhe a linha de A e também a linha do resultado C.
    for i in range(linhas_a):
        linha_resultado = []
        # j escolhe a coluna de B e também a coluna do resultado C.
        for j in range(colunas_b):
            total = 0
            termos = []
            expressao = ""
            # k percorre os pares da linha de A com a coluna de B.
            for k in range(colunas_a):
                produto = a[i][k] * b[k][j]
                total += produto
                termos.append({
                    "a": formatar_numero(a[i][k]),
                    "b": formatar_numero(b[k][j]),
                    "produto": formatar_numero(produto),
                    "acumulado": formatar_numero(total),
                })
                if k > 0:
                    expressao += " + "
                expressao += f"({formatar_numero(a[i][k])} × {formatar_numero(b[k][j])})"

            # Após somar todos os produtos, guardamos C[i][j].
            linha_resultado.append(total)
            passos.append({
                "linha": i + 1,
                "coluna": j + 1,
                "termos": termos,
                "valor": formatar_numero(total),
                "expressao": expressao + " = " + formatar_numero(total),
            })
        resultado.append(linha_resultado)

    return {
        "resultado": resultado,
        "passos": passos,
        "dimensoes": {"a": [linhas_a, colunas_a], "b": [linhas_b, colunas_b], "c": [linhas_a, colunas_b]},
    }
