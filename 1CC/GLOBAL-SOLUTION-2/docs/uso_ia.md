# Registro de uso de inteligência artificial

O ChatGPT auxiliou na interpretação do enunciado, na escolha de dois bairros fictícios, na geração dos registros, na elaboração do código Python e na revisão da documentação. A ferramenta também auxiliou na criação dos testes, do roteiro e da demonstração legendada.

## Como os resultados foram verificados durante a preparação

- O programa foi executado pelo mesmo menu de terminal disponível ao estudante. Em cópias de trabalho da base, foram realizados cadastro, busca, filtro, atendimento da fila e alterações de situação. Depois do encerramento e da reabertura, a ocorrência 013 conservou o histórico.
- As contagens do painel foram comparadas com os códigos dos CSV. A linha 099 foi recusada pelo cadastro. Na base inicial, as linhas das quatro categorias somam 12 e as três colunas de situação também somam 12.
- As durações das ocorrências concluídas foram calculadas separadamente a partir dos dias de abertura e conclusão. Os valores 5, 3 e 6 reproduziram a média de 4,67 dias exibida pelo programa.
- Tentativas de pular uma situação, usar um dia anterior e enviar campos em branco foram comparadas com o estado dos arquivos antes da ação. As tentativas recusadas deixaram os dados anteriores intactos.
- A apresentação usa trechos do terminal obtidos ao executar a aplicação em uma cópia dos dados. Os números exibidos depois da demonstração correspondem ao cadastro e à conclusão de 013.

## Verificação pelo estudante

As verificações acima descrevem a preparação assistida. Para a revisão individual, o estudante pode repetir a sequência de testes e explicar por que 099 fica fora do denominador, por que o início da análise retira o código da fila e por que só as concluídas entram na média. [Passos e resultados esperados](verificacao.md)
