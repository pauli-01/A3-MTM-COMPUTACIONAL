LIMITE_DIMENSAO = 6
INFINITO = float("inf")


def converter_numero(valor):
    # Aceita números com ponto ou vírgula decimal.
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
    # Confere dimensões, uniformidade e valores antes do cálculo.
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
    # i escolhe uma linha de A e abre uma linha na matriz resultado.
    for i in range(linhas_a):
        linha_resultado = []
        # j escolhe uma coluna de B e reinicia a soma para cada posição.
        for j in range(colunas_b):
            acumulador = 0
            # k emparelha os elementos correspondentes da linha e da coluna.
            for k in range(colunas_a):
                try:
                    acumulador += matriz_a[i][k] * matriz_b[k][j]
                except OverflowError:
                    raise ValueError("O cálculo excedeu o intervalo numérico.") from None
            if not -INFINITO < acumulador < INFINITO:
                raise ValueError("O cálculo excedeu o intervalo numérico.")
            linha_resultado.append(acumulador)
        resultado.append(linha_resultado)
    return resultado


def ler_dimensao(rotulo):
    while True:
        texto = input(f"{rotulo} (1 a {LIMITE_DIMENSAO}): ").strip()
        if texto.isdecimal():
            try:
                dimensao = int(texto)
                if 1 <= dimensao <= LIMITE_DIMENSAO:
                    return dimensao
            except ValueError:
                pass
        print(f"Digite um inteiro de 1 a {LIMITE_DIMENSAO}.")


def ler_matriz(nome, linhas, colunas):
    print(f"Preencha a matriz {nome} ({linhas} × {colunas}).")
    matriz = []
    for i in range(linhas):
        linha = []
        for j in range(colunas):
            # Permite corrigir uma célula sem repetir as anteriores.
            while True:
                texto = input(f"{nome}[{i + 1},{j + 1}]: ")
                try:
                    linha.append(converter_numero(texto))
                    break
                except ValueError as erro:
                    print(erro)
        matriz.append(linha)
    return matriz


def exibir_matriz(nome, matriz):
    # Ajusta a largura das células pelo maior valor exibido.
    linhas_texto = []
    largura = 0
    for linha in matriz:
        linha_texto = []
        for valor in linha:
            try:
                texto = str(valor).replace(".", ",")
            except ValueError:
                raise ValueError("O número está fora do intervalo de exibição.") from None
            linha_texto.append(texto)
            if len(texto) > largura:
                largura = len(texto)
        linhas_texto.append(linha_texto)

    print(f"\nMatriz {nome} ({len(matriz)} × {len(matriz[0])})")
    for linha_texto in linhas_texto:
        celulas = []
        for texto in linha_texto:
            celulas.append(texto.rjust(largura))
        print("[ " + "  ".join(celulas) + " ]")


def realizar_calculo():
    linhas_a = ler_dimensao("Linhas de A")
    colunas_a = ler_dimensao("Colunas de A")
    linhas_b = ler_dimensao("Linhas de B")
    colunas_b = ler_dimensao("Colunas de B")
    if colunas_a != linhas_b:
        raise ValueError(
            "Dimensões incompatíveis. "
            f"As colunas de A ({colunas_a}) devem corresponder às linhas de B ({linhas_b})."
        )

    matriz_a = ler_matriz("A", linhas_a, colunas_a)
    matriz_b = ler_matriz("B", linhas_b, colunas_b)
    resultado = multiplicar_matrizes(matriz_a, matriz_b)
    exibir_matriz("A", matriz_a)
    exibir_matriz("B", matriz_b)
    exibir_matriz("C", resultado)


def quer_continuar():
    while True:
        resposta = input("\nDeseja realizar outro cálculo? (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "não", "nao"):
            return False
        print("Responda com s ou n.")


def principal():
    print("Multiplicação de Matrizes")
    print("As colunas de A devem corresponder às linhas de B.")
    try:
        while True:
            try:
                realizar_calculo()
            except ValueError as erro:
                print(erro)
            if not quer_continuar():
                break
    except (EOFError, KeyboardInterrupt):
        print()
    print("Programa encerrado.")


if __name__ == "__main__":
    principal()
