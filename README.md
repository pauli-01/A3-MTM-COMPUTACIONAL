# MatrizLab

Projeto da A3 de Matemática Computacional da Unisul. O MatrizLab multiplica duas matrizes e mostra os produtos e a soma que formam cada posição do resultado.

[Abrir o MatrizLab](https://pauli-01.github.io/A3-MTM-COMPUTACIONAL/)

## Como usar

1. Escolha as dimensões de A e B e preencha os valores. O número de colunas de A deve ser igual ao número de linhas de B.
2. Clique em **Calcular A × B** e selecione um valor da matriz C para ver sua conta.
3. Para testar com os dados da apresentação, clique em **Carregar exemplo**. O site preenche as matrizes e calcula o resultado.

```text
A = [[1, 2, 3], [4, 5, 6]]
B = [[7, 8], [9, 10], [11, 12]]
C = [[58, 64], [139, 154]]
```

O cálculo é feito em Python com três laços, sem NumPy. O primeiro laço escolhe uma linha de A, o segundo escolhe uma coluna de B e o terceiro multiplica os pares e soma os produtos. O Pyodide executa o código Python no navegador.

## Como abrir localmente

Baixe ou clone o repositório. Com Python 3 instalado, abra um terminal na raiz do projeto e execute o comando do seu sistema.

**Windows**

```powershell
py -3 -m http.server 4173 --bind 127.0.0.1 --directory MatrizLab-site
```

**Linux ou macOS**

```bash
python3 -m http.server 4173 --bind 127.0.0.1 --directory MatrizLab-site
```

Com o terminal aberto, acesse [http://127.0.0.1:4173/](http://127.0.0.1:4173/). O cálculo funciona sem internet. Pressione **Ctrl+C** no terminal para encerrar o servidor.

## Arquivos do projeto

- A pasta [`MatrizLab-site/`](MatrizLab-site/) contém a interface e o Pyodide.
- O arquivo [`cod-mult-matriz.py`](cod-mult-matriz.py) na raiz deixa o algoritmo disponível para leitura. O site executa [`MatrizLab-site/cod-mult-matriz.py`](MatrizLab-site/cod-mult-matriz.py).
