# Como o programa funciona

O programa multiplica matrizes de forma manual. Pense nas matrizes como tabelas de números. Para obter uma posição de C, escolha uma linha de A e uma coluna de B, multiplique os pares de elementos na mesma ordem e some os produtos.

Se A é **m × n** e B é **n × p**, C tem **m × p**. As dimensões internas, ambas representadas por **n**, precisam coincidir porque cada elemento da linha escolhida precisa ter um par na coluna escolhida. As dimensões externas definem quantas linhas e colunas C terá.

## Arquivos e responsabilidades

| Arquivo ou pasta | Responsabilidade |
| --- | --- |
| `calculo.py` | Prepara os valores, verifica as matrizes e calcula C. Também monta o texto da conta de cada célula. |
| `hospedagem.py` e `render.yaml` | Permitem servir o mesmo site em um endereço público. |
| `terminal.py` | Lê as matrizes pelo teclado, efetua o mesmo cálculo manual e imprime A, B e C. Pode ser copiado e executado sozinho. |
| `servidor.py` | Entrega os arquivos do site e dos slides e liga a interface à função em Python. |
| `site/index.html` | Estrutura da página, controles, áreas para matrizes e passos. |
| `site/estilo.css` | Legibilidade, espaçamento, contraste e adaptação da página à largura da tela. |
| `site/interface.js` | Monta as grades, lê o formulário, faz o pedido ao servidor e atualiza o resultado. |
| `apresentacao/` | Estrutura, estilos e navegação dos slides. |
| `tests/` | Verificações automatizadas do cálculo, do terminal e da comunicação HTTP. |

## Listas de listas e índices

```python
matriz_a = [[1, 2, 3], [4, 5, 6]]
```

Cada lista interna representa uma linha. `len(matriz_a)` devolve 2 e `len(matriz_a[0])` devolve 3. As listas Python começam no índice **0**. `matriz_a[1][2]` acessa a segunda linha e a terceira coluna e devolve 6. Na interface, os números das linhas e das colunas começam em **1** para acompanhar a notação matemática. Assim, o mesmo valor é mostrado como `A[2,3]`.

## Leitura de `calculo.py`

As tabelas seguem a ordem das instruções. Linhas em branco separam blocos e os comentários do arquivo indicam a intenção do trecho seguinte.

### Constantes e conversão de um elemento

| Instrução ou trecho | O que faz |
| --- | --- |
| `LIMITE_DIMENSAO = 6` | Define o tamanho máximo em linhas e colunas nesta demonstração. |
| `INFINITO = float("inf")` | Cria um limite de comparação para detectar números não finitos. |
| `def converter_numero(valor):` | Define a função que recebe um elemento e devolve um número. |
| `if type(valor) is str:` | Processa como entrada digitada quando o valor é texto. |
| `texto = valor.strip().replace(",", ".")` | Retira espaços nas pontas e troca a vírgula pelo ponto usado pelo Python. |
| `digitos = texto.lstrip("+-").replace(".", "", 1)` | Prepara uma cópia para inspecionar os dígitos, retirando sinais iniciais e um ponto. |
| `if not digitos.isdecimal():` e `raise ValueError(...)` | Recusam texto vazio, letras e caracteres que não pertençam ao formato decimal esperado. |
| `try:` | Agrupa as conversões que podem falhar. |
| `if "." in texto:` e `valor = float(texto)` | Convertem texto com separador decimal para ponto flutuante. |
| `else:` e `valor = int(texto)` | Convertem o restante para inteiro. As conversões usam o texto original normalizado, portanto entradas como `--2` falham. |
| `except ValueError:` e `raise ValueError(...) from None` | Trocam a exceção de conversão por uma mensagem curta. |
| `if type(valor) not in (int, float) or not -INFINITO < valor < INFINITO:` e `raise ValueError(...)` | Aceitam apenas números inteiros ou de ponto flutuante finitos. Verdadeiro, falso, infinito e NaN são recusados. |
| `return valor` | Entrega o número validado a quem chamou a função. |

### Validação de uma matriz

| Instrução ou trecho | O que faz |
| --- | --- |
| `def validar_matriz(matriz, nome):` | Recebe a lista de linhas e uma letra para identificar a matriz nas mensagens. |
| Primeiro `if type(matriz) is not list or ...` e `raise ValueError(...)` | Confirmam que a matriz é uma lista com 1 a 6 linhas. Só depois é seguro acessar a primeira linha. |
| Segundo `if type(matriz[0]) is not list or ...` e `raise ValueError(...)` | Confirmam que a primeira linha é uma lista com 1 a 6 colunas. |
| `colunas = len(matriz[0])` | Usa a largura da primeira linha como referência. |
| `matriz_validada = []` | Cria a cópia que receberá números já convertidos. |
| `for i, linha in enumerate(matriz):` | Obtém cada linha e seu índice para conferir o formato e localizar erros. |
| `if type(linha) is not list or len(linha) != colunas:` e `raise ValueError(...)` | Recusam linhas que não sejam listas ou tenham outra largura. |
| `linha_validada = []` | Abre uma linha vazia para os elementos convertidos. |
| `for j, valor in enumerate(linha):` | Obtém cada elemento e seu índice de coluna. |
| `try:` e `linha_validada.append(converter_numero(valor))` | Tentam converter o elemento e guardam o valor em caso de sucesso. |
| `except ValueError as erro:` e `raise ValueError(f"{nome}[{i + 1},{j + 1}]: {erro}") from None` | Informam a matriz, linha e coluna da entrada problemática. |
| `matriz_validada.append(linha_validada)` | Guarda a linha completa. |
| `return matriz_validada` | Entrega a matriz pronta para as operações aritméticas. |

### Formatação para exibir números

| Instrução ou trecho | O que faz |
| --- | --- |
| `def formatar_numero(valor):` | Define a função usada para escrever números nos passos e no resultado do site. |
| `try:` e `return str(valor).replace(".", ",")` | Convertem o número em texto e usam vírgula decimal na apresentação. |
| `except ValueError:` e `raise ValueError(...) from None` | Informam quando o Python não consegue converter um número muito grande em texto. |

### Multiplicação, linha por linha

| Instrução ou trecho | O que faz |
| --- | --- |
| `def multiplicar_matrizes(matriz_a, matriz_b):` | Define a função que recebe A e B. |
| `matriz_a = validar_matriz(matriz_a, "A")` | Valida A e usa a cópia com os números convertidos. |
| `matriz_b = validar_matriz(matriz_b, "B")` | Faz o mesmo para B. |
| `linhas_a = len(matriz_a)` | Conta as linhas de A, que também serão as linhas de C. |
| `colunas_a = len(matriz_a[0])` | Conta as colunas de A e define quantos produtos entram em cada célula. |
| `linhas_b = len(matriz_b)` | Conta quantas linhas B oferece para formar os pares de uma coluna. |
| `colunas_b = len(matriz_b[0])` | Conta as colunas de B, que também serão as colunas de C. |
| `if colunas_a != linhas_b:` | Verifica se as dimensões internas são diferentes. |
| `raise ValueError(...)` | Interrompe o cálculo incompatível e informa os tamanhos em conflito. |
| `resultado = []` | Prepara a lista que vai receber as linhas de C. |
| `passos = []` | Prepara outra lista com o mesmo formato de C para os textos das contas. |
| `for i in range(linhas_a):` | Escolhe a linha de A que será combinada com as colunas de B. É o laço das linhas de C. |
| `linha_resultado = []` | Abre a nova linha de valores de C. |
| `linha_passos = []` | Abre a linha correspondente das contas. |
| `for j in range(colunas_b):` | Escolhe uma coluna de B e fixa a posição de C pelos índices `i` e `j`. |
| `acumulador = 0` | Começa a soma da posição atual. Zero é o elemento neutro da adição. Reiniciar dentro de `j` evita carregar os produtos da posição anterior. |
| `termos = []` | Abre a lista de textos que serão exibidos na conta da posição atual. |
| `for k in range(colunas_a):` | Para o par linha-coluna fixado, percorre as posições internas na mesma ordem. |
| `valor_a = matriz_a[i][k]` | Lê a posição `k` na linha `i` de A. |
| `valor_b = matriz_b[k][j]` | Lê a posição `k` na coluna `j` de B. |
| `try:` | Prepara o tratamento de uma operação numérica fora do intervalo. |
| `acumulador += valor_a * valor_b` | Multiplica o par com `*` e soma o produto ao acumulador. `x += y` equivale a `x = x + y` nesta conta. |
| `except OverflowError:` e `raise ValueError(...) from None` | Transformam falhas por limite numérico em uma mensagem que pode ser mostrada ao usuário. |
| `termos.append(f"({formatar_numero(valor_a)} × {formatar_numero(valor_b)})")` | Guarda o par em forma de texto para montar o passo a passo. |
| `if not -INFINITO < acumulador < INFINITO:` e `raise ValueError(...)` | Interrompem a operação se o resultado ficou não finito, o que pode ocorrer por estouro em ponto flutuante. |
| `linha_resultado.append(acumulador)` | Inclui o valor de C calculado após o último `k`. |
| `expressao = " + ".join(termos)` | Junta os textos dos produtos com o sinal de adição. A soma numérica já ocorreu no laço. |
| `linha_passos.append(f"C[{i + 1},{j + 1}] = ...")` | Guarda a expressão com índices a partir de 1 e o valor do acumulador. |
| `resultado.append(linha_resultado)` | Guarda a linha de C depois que todas as colunas de B foram percorridas. |
| `passos.append(linha_passos)` | Guarda a linha de passos na mesma ordem. |
| `return resultado, passos` | Entrega as duas matrizes para o servidor. |

## Simulação do exemplo

A tem duas linhas e três colunas. B tem três linhas e duas colunas. Três é a dimensão compartilhada, então cada célula de C resulta da soma de três produtos, e C tem duas linhas e duas colunas.

| Posição | Linha de A | Coluna de B | Expressão |
| --- | --- | --- | --- |
| C[1,1] | (1, 2, 3) | (7, 9, 11) | (1 × 7) + (2 × 9) + (3 × 11) = 58 |
| C[1,2] | (1, 2, 3) | (8, 10, 12) | (1 × 8) + (2 × 10) + (3 × 12) = 64 |
| C[2,1] | (4, 5, 6) | (7, 9, 11) | (4 × 7) + (5 × 9) + (6 × 11) = 139 |
| C[2,2] | (4, 5, 6) | (8, 10, 12) | (4 × 8) + (5 × 10) + (6 × 12) = 154 |

Para C[1,1], em Python `i = 0` e `j = 0`. O acumulador começa em 0. Em `k = 0`, soma 7. Em `k = 1`, soma 18 e chega a 25. Em `k = 2`, soma 33 e chega a 58. Depois `j` avança para 1 e o acumulador volta a zero.

## Comparação de fornecedores

Use A = `[[2, 1], [1, 3]]` para as quantidades e B = `[[10, 12], [5, 4]]` para os preços unitários em reais. Em A, cada linha é um pedido e cada coluna é um produto na ordem caneta, caderno. Em B, as linhas seguem essa mesma ordem de produtos, e cada coluna representa um fornecedor. Assim, C = `[[25, 28], [25, 24]]` mostra o custo total de cada pedido em cada fornecedor. C[1,2], por exemplo, é R$ 28 para comprar duas canetas de R$ 12 e um caderno de R$ 4 no segundo fornecedor.

## Do clique em Calcular à resposta na tela

1. O formulário oferece dimensões e uma grade para cada matriz. O JavaScript lê as células e prepara um objeto com duas listas de listas, `a` e `b`.
2. O navegador envia as matrizes em JSON para `POST /api/calcular`. JSON é um formato de texto para trocar dados.
3. `ServidorMatrizes.do_POST` encaminha o pedido a `responder_calculo`, que verifica o endereço, o formato, o tamanho e a estrutura. Em seguida chama `multiplicar_matrizes`. O backend valida as matrizes mesmo quando os dados chegam de fora do formulário.
4. Se o cálculo terminar, `resposta_json` prepara o envio de `resultado`, `resultado_formatado` e `passos`. Os textos preservam a representação dos números produzida pelo Python quando o navegador lê o JSON. Se a entrada for inválida, a resposta inclui uma mensagem no campo `erro`.
5. O JavaScript mostra A e B, seus tamanhos, a matriz C e as contas devolvidas pelo Python. Se ocorrer um erro, mostra a mensagem no formulário.

`do_GET` chama `servir_arquivo`, que entrega arquivos do site e da apresentação por caminhos predefinidos. `criar_servidor` inicia a escuta no endereço local, e `principal` mantém o servidor em execução até **Ctrl+C**. `http.server`, `json` e `pathlib` cuidam da infraestrutura web, da troca de dados e da leitura dos arquivos. Confirme com o professor como a restrição do PDF sobre bibliotecas se aplica a esses módulos. O cálculo usa listas, controle de fluxo e aritmética básica.

Quando o site é hospedado, o Gunicorn recebe as conexões e chama `aplicacao` em `hospedagem.py`. A função recebe os dados da requisição no formato WSGI, usa `servir_arquivo` ou `responder_calculo` e devolve o status, os cabeçalhos e o corpo da resposta. O cálculo usa a mesma função Python em ambos os ambientes.

## Versão independente de terminal

`ler_dimensao` repete a pergunta até receber um inteiro no intervalo. `ler_matriz` coleta um elemento por vez e permite corrigir a célula atual. `realizar_calculo` confere as dimensões antes de pedir os elementos, chama a multiplicação e encaminha as três matrizes para `exibir_matriz`, que alinha o texto pelo tamanho da maior célula. `quer_continuar` trata a resposta **s/n**. `principal` repete o fluxo, lida com erros de entrada e encerra quando o usuário decide sair.

O algoritmo do terminal é independente para permitir a execução de `terminal.py` sozinho. Usa os mesmos três laços e devolve C. A suíte compara os valores de C nas duas implementações para os mesmos dados.

## Perguntas para a apresentação

| Pergunta | Resposta |
| --- | --- |
| Por que a ordem de A e B importa? | No produto A × B, usamos linhas de A e colunas de B. Trocar a ordem pode mudar o resultado ou tornar as dimensões incompatíveis. |
| Por que há três laços? | Precisamos escolher a linha, escolher a coluna e percorrer os pares internos para calcular a célula. |
| Por que zerar o acumulador em cada posição? | Cada posição é uma nova soma, formada apenas pelos produtos da sua linha e da sua coluna. |
| Por que os índices começam em 1 na interface? | É a notação usada para mostrar as posições ao usuário. A primeira posição da lista em Python tem índice 0. |
| Como conferir o resultado rapidamente? | Multiplique por uma identidade de tamanho compatível. A matriz de entrada deve ser preservada. Com uma matriz zero compatível, o resultado deve ter apenas zeros. |
| Quantas multiplicações são realizadas? | São `m × p` células e `n` pares por célula, portanto `m × n × p` multiplicações. |
| Por que os testes de decimais usam tolerância? | Alguns números decimais só têm representação aproximada em ponto flutuante. A tolerância aceita pequenas diferenças dessa representação. |
| O que o JavaScript calcula? | Ele organiza a interface e troca dados com o servidor. A multiplicação e a geração dos passos são feitas em Python. |
