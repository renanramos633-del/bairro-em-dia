# Bairro em Dia

**Neighborhood Action Dashboard · CitizenTech · Global Solution 2026.2 · FIAP**

| Identificação | Dados da entrega |
|---|---|
| Equipe | Bairro em Dia · projeto individual |
| Integrante | Renan Queiroz Ramos |
| RM | 574959 |
| Vídeo no YouTube | A preencher com o link da apresentação não listada |

A apresentação acompanha o código 013 do cadastro à conclusão. [Vídeo de demonstração legendado](docs/Bairro-em-Dia-demonstracao.mp4)

## Problema e público

Na comunidade fictícia de Vila Ipê e Jardim da Ponte, um poste apagado na praça e uma rampa com piso solto podem ser relatados no mesmo dia. Quem passa pelo local precisa conseguir distinguir o que ainda aguarda triagem do que já está em análise. O painel reúne os relatos em um só lugar e permite acompanhar cada um pelo código.

Moradores, frequentadores dos espaços coletivos e pessoas que organizam o acompanhamento comunitário são o público do protótipo. O exemplo de acessibilidade considera quem depende de uma rota de pedestres contínua, inclusive pessoas que utilizam bengala ou cadeira de rodas.

## Como executar

Com Python 3.7 ou superior, abra o terminal na pasta deste README (`1CC/GLOBAL-SOLUTION-2`) e rode o comando abaixo.

```bash
python src/sistema.py
```

Se o comando do seu sistema for `python3`, use `python3 src/sistema.py`. O programa usa a biblioteca padrão. Escolha as ações pelo número e pressione Enter. A opção **0** encerra. Cada cadastro e atualização válidos são gravados imediatamente nos arquivos CSV. Para repetir os exemplos com os números originais, use uma cópia recém-extraída do projeto.

| Menu | Ação |
|---|---|
| 1 · Listar | Mostra código, categoria, situação, bairro e local de cada ocorrência válida. |
| 2 · Cadastrar | Pede categoria, bairro, local genérico, descrição e dia simulado de abertura. Gera o código. |
| 3 · Buscar | Localiza um código e mostra a descrição e as mudanças de situação em ordem de acompanhamento. |
| 4 · Filtrar | Combina categoria e situação. A opção **0** em cada pergunta inclui todas as opções daquele campo. |
| 5 · Atualizar | Muda a situação pelo código e grava o dia da alteração. |
| 6 · Fila de triagem | Exibe as abertas por ordem de cadastro e permite examinar a primeira. |
| 7 · Histórico recente | Exibe as atualizações da última registrada para a primeira. |
| 8 · Bairros e categorias | Agrupa os códigos por bairro e, dentro dele, por categoria. |
| 9 · Indicadores | Recalcula a matriz, os percentuais, as pendências e o tempo médio. |

## Dados simulados

Os dois CSV usam UTF-8, cabeçalho e ponto e vírgula como separador. A primeira linha de dados representa o primeiro registro do arquivo. A simulação conta dias inteiros a partir de 1. Uma abertura e uma conclusão no mesmo dia têm duração zero.

| Campo de `ocorrencias.csv` | Obrigatório | Conteúdo |
|---|---|---|
| `codigo` | Sim, automático no menu | Inteiro positivo identificado com pelo menos três dígitos. A busca aceita tanto `1` quanto `001`. |
| `categoria` | Sim | Iluminação, Acessibilidade, Limpeza ou Conservação. A última trata da conservação de espaços coletivos. |
| `descricao` | Sim | Relato breve do problema observado. |
| `bairro` e `local` | Sim, ambos | Bairro da simulação e um ponto público genérico, como Praça do Coreto. |
| `dia_abertura` | Sim | Dia inteiro positivo. |
| `status_inicial` | Sim, automático no menu | Toda ocorrência nasce Aberta e entra no fim da fila. |

Em `historico.csv`, cada linha contém três campos obrigatórios, `codigo`, `dia` e `novo_status`. Ao iniciar, o programa lê as aberturas e aplica as mudanças na ordem em que foram registradas. Assim a situação atual pode ser reconstruída sem apagar as anteriores.

Há **13 linhas de abertura** na amostra. A linha 14 do CSV, código **099**, tem a categoria em branco. O programa exibe o arquivo, a linha, o código e o motivo da rejeição. As outras **12 ocorrências** formam a base dos indicadores. O histórico inicial possui **10 mudanças válidas**. [Cadastros](dados/ocorrencias.csv) · [Histórico](dados/historico.csv)

## Situações e regras de decisão

| Situação | Significado | Próximo passo permitido |
|---|---|---|
| Aberta | O relato foi registrado e aguarda a primeira análise. | Em análise |
| Em análise | A triagem já começou e o acompanhamento continua. | Concluída |
| Concluída | O acompanhamento foi encerrado na simulação. | Fim do fluxo |

As condições `if`, `elif` e `else` verificam as entradas antes de gravar. Três exemplos do código explicam o uso dos operadores booleanos.

| Expressão em Python | Efeito para quem usa o painel |
|---|---|
| `not descricao or not local` | Se um dos textos fica vazio depois de remover os espaços, a mensagem pede descrição e local. O cadastro pode ser refeito no menu. |
| `atual == "Aberta" and novo != "Em análise"` | Depois de verificar se a situação é conhecida e diferente da atual, o sistema recusa um salto direto de Aberta para Concluída. |
| `categoria_ok and situacao_ok` | Um registro aparece se atender aos dois critérios. Em cada critério, por exemplo `not categoria or registro["categoria"] == categoria`, a escolha “Todas” deixa o filtro livre. |

Códigos repetidos, situações desconhecidas e dias anteriores ao último evento também geram mensagens. Uma busca por código ausente informa “Ocorrência não encontrada”. Falhas de validação preservam o cadastro e o histórico anteriores. [Regras e estruturas em Python](src/ocorrencias.py)

## Estruturas de dados

| Estrutura | Uso no Bairro em Dia | Por que foi escolhida |
|---|---|---|
| Lista `ocorrencias` | Guarda os registros na ordem de cadastro. | Um laço percorre toda a base para listar, filtrar ou contar. |
| Dicionário `por_codigo` | Relaciona cada código ao mesmo registro presente na lista. | A consulta encontra a ocorrência diretamente e a atualização fica visível nas duas formas de acesso. |
| Fila `fila` | Recebe os códigos das abertas no fim. A triagem examina o primeiro e o retira da frente. | Mantém a ordem de chegada. Se a análise for iniciada pelo código na opção 5, apenas aquele código sai da fila e os demais conservam sua posição. |
| Pilha `historico` | Cada atualização entra no fim da lista. A opção 7 lê a partir desse topo. | Mostra primeiro a alteração mais recente e preserva as anteriores para consulta. |
| Dicionários aninhados | Representam bairro → categoria → lista de códigos. | A opção 8 permite, por exemplo, localizar os relatos de iluminação da Vila Ipê, códigos 001 e 009 na base inicial. |
| Matriz de contagem | Cada linha representa uma categoria e cada coluna, uma situação. | Uma única passagem pelos registros preenche as células. A matriz é recalculada quando se abre o painel de indicadores. |

## Indicadores da base inicial

Cada ocorrência válida acrescenta 1 à célula de sua categoria e situação atual. A parcela de um grupo é `100 × quantidade do grupo ÷ total válido`. O painel usa o mesmo denominador para categorias e situações.

| Categoria | Aberta | Em análise | Concluída | Total | Parcela |
|---|---:|---:|---:|---:|---:|
| Iluminação | 2 | 2 | 0 | 4 | 33,3% |
| Acessibilidade | 1 | 1 | 1 | 3 | 25,0% |
| Limpeza | 1 | 1 | 1 | 3 | 25,0% |
| Conservação | 1 | 0 | 1 | 2 | 16,7% |
| **Total** | **5** | **4** | **3** | **12** | **100,0%** |
| **Parcela por situação** | **41,7%** | **33,3%** | **25,0%** | | |

**Pendências.** O painel soma as 5 abertas às 4 em análise. São 9 de 12 ocorrências, ou 75%. Iluminação concentra 4 dessas 9 pendências, o maior número entre as categorias. Consultar os locais desses quatro registros é um ponto de partida para discutir o acompanhamento simulado.

**Tempo médio até a conclusão.** Para cada concluída, subtraímos o dia de abertura do dia de conclusão e dividimos a soma pelo número de concluídas.

| Código | Abertura | Conclusão | Dias decorridos |
|---|---:|---:|---:|
| 002 | 1 | 6 | 5 |
| 003 | 2 | 5 | 3 |
| 004 | 2 | 8 | 6 |

A média inicial é `(5 + 3 + 6) ÷ 3 = 4,67 dias simulados`. Uma base sem concluídas apresenta a mensagem “Tempo médio indisponível”. Percentuais são arredondados para uma casa e a média para duas.

## Exemplo para reproduzir no terminal

1. Na base inicial, escolha **4** e filtre por **Iluminação** e **Aberta**. Os resultados são **009** e **012**.
2. Escolha **2** para cadastrar. Selecione **2 · Acessibilidade** e **1 · Vila Ipê**. Digite `Praça da Estação`, `Piso tátil solto na entrada.` e o dia `9`. O programa atribui **013**.
3. Escolha **5**, código `013`, situação **2 · Em análise**, dia `10`. Repita a opção **5** para o mesmo código, agora com **3 · Concluída**, dia `12`.
4. Escolha **3** e busque `13`. A consulta mostra o local, a descrição e os três marcos abaixo.

```text
Dia 9 | Abertura
Dia 10 | Aberta → Em análise
Dia 12 | Em análise → Concluída
```

5. Abra **9 · Indicadores**. Com a conclusão de 013, são 13 ocorrências, 5 abertas, 4 em análise e 4 concluídas. Os 3 dias de 013 elevam a soma para 17 dias. A nova média é `17 ÷ 4 = 4,25 dias`.
6. Encerre com **0**, abra o programa novamente e busque `013`. O histórico permanece disponível. [Verificações reproduzíveis](docs/verificacao.md)

## Acessibilidade, inclusão e privacidade

O menu usa números em ordem, uma opção por linha, e funciona inteiramente pelo teclado. Situações e erros aparecem por escrito. A leitura do detalhe por código complementa a tabela com a descrição e a sequência de eventos.

Os exemplos utilizam bairros fictícios e referências a espaços de uso coletivo. O formulário orienta quem cadastra a descrever o local de forma genérica. Os campos livres exigem cuidado humano para evitar nomes de moradores, contatos, endereços residenciais ou outras informações pessoais.

## Conclusões e limites

A fila responde a “quem aguarda a primeira análise?”. A matriz responde a “quantas demandas ainda precisam de acompanhamento?”. Na base inicial, são **5** na primeira resposta e **9** na segunda, pois quatro já saíram da fila e continuam em análise. Essa diferença mostra por que guardar apenas uma contagem geral seria insuficiente.

O protótipo considera uso individual, dois bairros fictícios e três situações. A quantidade de relatos permite comparar a amostra. Para avaliar urgência ou impacto real, seriam necessárias outras informações. Os dias simulados e as conclusões descrevem o exercício acadêmico. O sistema não envia solicitações a serviços públicos.

O exercício permite explicar como um mesmo registro pode estar em uma lista e em um índice por código, como a ordem de leitura distingue fila e pilha e por que uma linha inválida altera percentuais se entrar na contagem. [Participação da IA](docs/uso_ia.md) · [Roteiro da apresentação](docs/roteiro_video.md)
