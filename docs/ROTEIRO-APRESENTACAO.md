# Roteiro da apresentação

**Duração sugerida de 9 minutos.** Este tempo é uma escolha de organização da equipe.

Abra `apresentacao/index.html` no navegador e preencha os nomes da equipe na capa. Os campos editados ficam na aba aberta. Use as setas esquerda e direita ou os botões **Anterior** e **Próximo**. Para exportar todos os slides, use **Imprimir / PDF** e selecione **Salvar como PDF** no navegador.

## Divisão entre integrantes

| Equipe | Integrante 1 | Integrante 2 | Integrante 3 |
| --- | --- | --- | --- |
| Duas pessoas | Slides 1 a 6 · 4 min 50 s | Slides 7 a 10 · 4 min 10 s | — |
| Três pessoas | Slides 1 a 4 · 2 min 55 s | Slides 5 a 7 · 2 min 40 s | Slides 8 a 10 · 3 min 25 s |

Quem conduz a demonstração fica com o navegador e o terminal preparados antes da apresentação.

## Fala por slide

| Slide | Tempo | Fala sugerida |
| --- | --- | --- |
| 1. Multiplicação de Matrizes | 35 s | “Somos [nomes]. Para a opção 3 de Matemática Computacional Aplicada, desenvolvemos em Python um software para multiplicar matrizes.” |
| 2. Quanto custa cada pedido? | 45 s | “Queremos que o usuário consiga calcular e entender o resultado. Nesta aplicação, as linhas de A são pedidos e as colunas são produtos. As linhas de B seguem a mesma ordem dos produtos e as colunas são fornecedores. Cada valor em C é o total de um pedido se todos os itens forem comprados do fornecedor daquela coluna.” |
| 3. Linhas e colunas | 45 s | “Uma matriz organiza números em linhas e colunas. Falamos sempre a quantidade de linhas primeiro. Esta matriz é 2 por 3. A segunda linha é 4, 5, 6 e o valor na segunda linha, terceira coluna, é 6.” |
| 4. Quando podemos multiplicar? | 50 s | “Para combinar uma linha de A com uma coluna de B, as duas precisam ter o mesmo número de valores. Se A é m por n e B é n por p, o resultado tem m linhas e p colunas. Uma matriz 2 por 3 com outra 3 por 2 produz uma matriz 2 por 2.” |
| 5. Uma linha encontra uma coluna | 55 s | “Para achar a primeira posição de C, usamos a primeira linha de A e a primeira coluna de B. Multiplicamos cada par na ordem e somamos. Um vezes sete dá sete, dois vezes nove dá dezoito e três vezes onze dá trinta e três. A soma é cinquenta e oito.” |
| 6. O cálculo em Python | 1 min | “O programa cria uma lista vazia para o resultado e uma lista para cada nova linha. Para cada posição, começa a soma em zero. O comando dentro do terceiro laço multiplica o par de valores e acrescenta o produto à soma. A soma vai para a linha do resultado, e a linha pronta vai para a matriz C.” |
| 7. O papel dos três laços | 45 s | “O i escolhe a linha em A, o j escolhe a coluna em B e o k percorre os pares que precisamos multiplicar. A posição inicial da lista em Python é zero. Nos passos exibimos a numeração a partir de um.” |
| 8. Demonstração | 2 min | “Vamos carregar o exemplo e verificar tanto a matriz C quanto os passos. Depois, vamos tentar multiplicar duas matrizes incompatíveis e ver a orientação do programa.” Siga a sequência abaixo. |
| 9. Validações e testes | 45 s | “O limite desta demonstração é de uma a seis linhas e colunas. A página envia os dados ao servidor local e o Python valida os dados e faz o cálculo. Testamos também casos como identidade, zero, valores decimais e dados inválidos.” |
| 10. Da regra ao software | 40 s | “Aprendemos a transformar a regra de linha por coluna em três laços e a traduzir cada iteração em um passo que o usuário consegue conferir. O programa pode ser usado no site local ou pelo terminal.” |

## Demonstração no navegador

Antes da apresentação, abra um terminal na pasta do projeto e rode `py -3 servidor.py` no Windows ou `python3 servidor.py` no Ubuntu. Abra `http://127.0.0.1:8000/` em uma aba de teste e mantenha o terminal do servidor aberto. No slide 8, use o link para o site local ou alterne para a aba preparada.

1. Clique em **Carregar exemplo**. Mostre que A tem dimensão 2 × 3, com linhas `1 2 3` e `4 5 6`. B tem dimensão 3 × 2, com linhas `7 8`, `9 10` e `11 12`.
2. Clique em **Calcular**. Confira que C tem dimensão 2 × 2, com linhas `58 64` e `139 154`.
3. Aponte o primeiro passo, já calculado em voz alta no slide 5. Confira as quatro posições com os valores abaixo.

   - C[1,1] = (1 × 7) + (2 × 9) + (3 × 11) = **58**
   - C[1,2] = (1 × 8) + (2 × 10) + (3 × 12) = **64**
   - C[2,1] = (4 × 7) + (5 × 9) + (6 × 11) = **139**
   - C[2,2] = (4 × 8) + (5 × 10) + (6 × 12) = **154**

4. Mantenha A com 2 × 3 e mude B para 2 × 2, alterando somente o número de linhas de B. Mostre o aviso de incompatibilidade. Ao tentar calcular, a ferramenta impede a multiplicação porque as 3 colunas de A exigem 3 linhas em B.
5. Volte à aba dos slides e avance para **Validações e testes**.

Se houver tempo, explique o total de R$ 25 do primeiro pedido no primeiro fornecedor no slide 2. O pedido contém duas unidades do primeiro produto e uma do segundo, então o total é `2 × 10 + 1 × 5`. Os mesmos itens custam `2 × 12 + 1 × 4 = 28` no segundo fornecedor.

## Alternativa pelo terminal

Se o navegador falhar, abra outro terminal na pasta do projeto. Rode `py -3 terminal.py` no Windows ou `python3 terminal.py` no Ubuntu.

1. Pressione Enter depois de cada resposta. Para as dimensões, digite `2`, `3`, `3`, `2`, nessa ordem. Em seguida, digite os elementos de A `1`, `2`, `3`, `4`, `5`, `6` e os de B `7`, `8`, `9`, `10`, `11`, `12`.
2. Mostre as três matrizes. Confira `58 64` e `139 154` em C. Use as expressões deste roteiro para explicar os quatro passos.
3. Digite `s` para repetir. Digite as dimensões `2`, `3`, `2`, `2` para mostrar o erro de incompatibilidade. Digite `n` para encerrar.
