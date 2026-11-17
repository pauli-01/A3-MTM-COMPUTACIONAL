# Multiplicação de Matrizes

Projeto da disciplina Matemática Computacional Aplicada, opção 3 (software matemático). O programa calcula o produto de duas matrizes e o site mostra a conta de cada elemento de C.

## Requisitos

- Python 3.8 ou posterior. O projeto foi testado com Python 3.12.14.
- Um navegador atualizado com JavaScript para o site e os slides.
- VS Code é opcional. Para abrir o projeto nele, use **Arquivo → Abrir Pasta** e selecione a pasta que contém `servidor.py`. No VS Code, use **Terminal → Novo Terminal** para rodar os comandos.

A execução local funciona offline e dispensa instalação de pacotes. O núcleo matemático e o programa de terminal não importam módulos. O servidor usa a biblioteca padrão do Python para HTTP, JSON e leitura de arquivos. Confirme com o professor se o uso desses módulos de infraestrutura atende à redação do PDF sobre bibliotecas. O terminal pode ser usado separadamente para a demonstração.

## Executar

Execute os comandos na pasta do projeto.

| Ação | Windows (PowerShell) | Ubuntu (terminal) |
| --- | --- | --- |
| Conferir Python | `py -3 --version` | `python3 --version` |
| Iniciar o site | `py -3 servidor.py` | `python3 servidor.py` |
| Usar o terminal | `py -3 terminal.py` | `python3 terminal.py` |
| Rodar os testes | `py -3 -m unittest discover -s tests -v` | `python3 -m unittest discover -s tests -v` |

No Windows, se o comando `py` estiver indisponível e `python --version` mostrar Python 3, substitua `py -3` por `python`.

- **Site.** Abra [http://127.0.0.1:8000/](http://127.0.0.1:8000/) com o servidor em execução. Clique em **Carregar exemplo** e depois em **Calcular**. Para fechar o servidor, pressione **Ctrl+C** no terminal.
- **Terminal.** Informe as dimensões e digite os elementos na ordem solicitada. Ao fim de um cálculo, o programa pergunta se você deseja continuar. O arquivo `terminal.py` também funciona sozinho.
- **Slides.** Abra [apresentacao/index.html](apresentacao/index.html) diretamente no navegador ou use [http://127.0.0.1:8000/apresentacao/](http://127.0.0.1:8000/apresentacao/) com o servidor ativo. Preencha os nomes na capa. Navegue com as setas ou os botões e use **Imprimir / PDF** para exportar.

O servidor escuta apenas em `127.0.0.1`. GitHub Pages hospeda arquivos estáticos e não executa o servidor Python.

## Publicar o site no Render

O repositório inclui `render.yaml` para criar um serviço gratuito com Gunicorn. O Render executa o cálculo em Python e fornece a URL HTTPS para compartilhar.

1. Entre no [painel do Render](https://dashboard.render.com/blueprints/new) e conecte sua conta do GitHub.
2. Autorize o acesso ao repositório `pauli-01/A3-MTM-COMPUTACIONAL`, selecione a branch `main` e use o Blueprint `render.yaml`.
3. Confirme que o plano é **Free**, aplique a configuração e aguarde o serviço ficar disponível.
4. Abra a URL mostrada na página do serviço. Use **Carregar exemplo** e **Calcular** para verificar o cálculo antes de compartilhar a URL.

A versão hospedada pode demorar para responder no primeiro acesso após um período de inatividade.

## Exemplo e formato de entrada

```text
    ⎡1  2  3⎤       ⎡ 7   8⎤       ⎡ 58   64⎤
A = ⎣4  5  6⎦   B = ⎢ 9  10⎥   C = ⎣139  154⎦
                    ⎣11  12⎦
```

As colunas de A precisam coincidir em quantidade com as linhas de B. O programa aceita matrizes de 1 a 6 linhas e colunas, limite escolhido para facilitar a demonstração. Digite números como `-2`, `0`, `1,5` ou `1.5`, sem separadores de milhar. Os cálculos decimais usam ponto flutuante e podem exibir diferenças de arredondamento.

## Entrega e estrutura

Copie `A3-MTM-COMPUTACIONAL-entrega.zip` para o outro computador e extraia os arquivos. Dentro da pasta extraída, abra o terminal, verifique se o Python está instalado e siga os comandos da tabela. Leve também o [roteiro](docs/ROTEIRO-APRESENTACAO.md) para a demonstração.

| Caminho | Conteúdo |
| --- | --- |
| `calculo.py` | Validação, multiplicação e passos exibidos no site |
| `servidor.py` | Servidor local e comunicação com a interface |
| `terminal.py` | Programa independente de terminal |
| `hospedagem.py` e `render.yaml` | Entrada WSGI e configuração da hospedagem pública opcional |
| `site/` | HTML, CSS e JavaScript da calculadora |
| `apresentacao/` | Slides offline com navegação por teclado e impressão |
| `docs/` | [Explicação do código](docs/EXPLICACAO-CODIGO.md) e roteiro |
| `tests/` | Testes de cálculo, terminal e servidor |
| `LISTAGEM-CODIGO.txt` | Cópia integral dos arquivos de código |
| `A3-MTM-COMPUTACIONAL-entrega.zip` | Projeto compactado para transferência |
