LIMITE_DIMENSAO = 6
INFINITO = float("inf")


def converter_numero(valor):
    # Converte texto com vírgula ou ponto e preserva inteiros.
    if type(valor) is str:
        texto = valor.strip().replace(",", ".")
        digitos = texto.lstrip("+-").replace(".", "", 1)
        if not digitos.isdecimal():
            raise ValueError("Digite um número com ponto ou vírgula decimal.")
        try:
            if "." in texto:
                valor = float(texto)
            else:
                valor = int(texto)
        except ValueError:
            raise ValueError("Digite um número válido.") from None

    if type(valor) not in (int, float) or not -INFINITO < valor < INFINITO:
        raise ValueError("Digite um número finito.")
    return valor


def validar_matriz(matriz, nome):
    # Verifica o formato e cria uma cópia com os elementos convertidos.
    if type(matriz) is not list or not 1 <= len(matriz) <= LIMITE_DIMENSAO:
        raise ValueError(f"A matriz {nome} deve ter de 1 a {LIMITE_DIMENSAO} linhas.")
    if type(matriz[0]) is not list or not 1 <= len(matriz[0]) <= LIMITE_DIMENSAO:
        raise ValueError(f"A matriz {nome} deve ter de 1 a {LIMITE_DIMENSAO} colunas.")

    colunas = len(matriz[0])
    matriz_validada = []
    for i, linha in enumerate(matriz):
        if type(linha) is not list or len(linha) != colunas:
            raise ValueError(f"Todas as linhas da matriz {nome} devem ter {colunas} colunas.")
        linha_validada = []
        for j, valor in enumerate(linha):
            try:
                linha_validada.append(converter_numero(valor))
            except ValueError as erro:
                raise ValueError(f"{nome}[{i + 1},{j + 1}]: {erro}") from None
        matriz_validada.append(linha_validada)
    return matriz_validada


def formatar_numero(valor):
    # Usa a vírgula decimal nas expressões apresentadas.
    try:
        return str(valor).replace(".", ",")
    except ValueError:
        raise ValueError("O número está fora do intervalo de exibição.") from None


def multiplicar_matrizes(matriz_a, matriz_b):
    matriz_a = validar_matriz(matriz_a, "A")
    matriz_b = validar_matriz(matriz_b, "B")
    linhas_a = len(matriz_a)
    colunas_a = len(matriz_a[0])
    linhas_b = len(matriz_b)
    colunas_b = len(matriz_b[0])
    if colunas_a != linhas_b:
        raise ValueError(
            "Dimensões incompatíveis. "
            f"As colunas de A ({colunas_a}) devem corresponder às linhas de B ({linhas_b})."
        )

    resultado = []
    passos = []
    # i percorre as linhas de A e abre uma linha do resultado.
    for i in range(linhas_a):
        linha_resultado = []
        linha_passos = []
        # j percorre as colunas de B e escolhe uma posição de C.
        for j in range(colunas_b):
            # Cada posição começa com soma zero.
            acumulador = 0
            termos = []
            # k combina os elementos da linha de A e da coluna de B.
            for k in range(colunas_a):
                valor_a = matriz_a[i][k]
                valor_b = matriz_b[k][j]
                try:
                    acumulador += valor_a * valor_b
                except OverflowError:
                    raise ValueError("O cálculo excedeu o intervalo numérico.") from None
                termos.append(f"({formatar_numero(valor_a)} × {formatar_numero(valor_b)})")

            if not -INFINITO < acumulador < INFINITO:
                raise ValueError("O cálculo excedeu o intervalo numérico.")

            # Guarda o valor e a expressão da posição recém-calculada.
            linha_resultado.append(acumulador)
            expressao = " + ".join(termos)
            linha_passos.append(f"C[{i + 1},{j + 1}] = {expressao} = {formatar_numero(acumulador)}")
        resultado.append(linha_resultado)
        passos.append(linha_passos)
    return resultado, passos
