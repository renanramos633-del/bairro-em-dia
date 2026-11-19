# Como conferir o protótipo

Comece com uma cópia recém-extraída da atividade. Abra o terminal na pasta da Global Solution e rode `python src/sistema.py`. As verificações abaixo foram executadas na preparação do protótipo. Você pode repeti-las comparando o que aparece no seu terminal com a coluna de resultado.

## Conferir a base inicial

| O que testar | Entrada | Resultado observado |
|---|---|---|
| Validação da amostra | Abrir o sistema. | O código 099, linha 14 do CSV, é ignorado por falta de categoria. Restam 12 ocorrências e 10 atualizações. |
| Busca por código | Opção 3, código `1`. Depois, buscar `099`. | A primeira busca localiza 001 na Praça do Coreto. A segunda informa que a ocorrência não foi encontrada. |
| Filtro combinado | Opção 4, Iluminação e Aberta. | Aparecem apenas 009 e 012. |
| Filtro livre e filtro vazio | Opção 4, Todas e Concluída. Depois, Iluminação e Concluída. | A primeira combinação encontra 002, 003 e 004. A segunda informa que nenhuma ocorrência foi encontrada. |
| Fila | Opção 6, depois escolha Voltar. | A ordem é 008, 009, 010, 011 e 012. A primeira a ser examinada pela fila será 008. |
| Pilha e hierarquia | Opções 7 e 8. | O primeiro evento da pilha é o de 004 no dia 8. Em Vila Ipê, a categoria Iluminação agrupa 001 e 009. |
| Indicadores | Opção 9. | Abertas 5, em análise 4, concluídas 3, pendências 9 e tempo médio de 4,67 dias. |

## Acompanhar um novo registro

Siga esta sequência na mesma cópia para manter os códigos e os dias do exemplo.

| Ação | Entrada resumida | Resultado observado |
|---|---|---|
| Cadastro inválido | Na opção 2, preencha os campos e deixe o local em branco. | O programa pede descrição e local. O total continua 12. |
| Cadastro válido | Opção 2, Acessibilidade, Vila Ipê, Praça da Estação, “Piso tátil solto na entrada.”, dia 9. | O código 013 é criado como Aberta e entra no fim da fila. |
| Salto de situação | Opção 5, código 013, Concluída, dia 10. | A mensagem explica que a ocorrência precisa passar por Em análise. A tentativa não gera evento. |
| Início da análise | Opção 5, código 013, Em análise, dia 10. | A situação muda e 013 sai da fila. Os códigos anteriores conservam a ordem. |
| Data anterior | Opção 5, código 013, Concluída, dia 9. | O programa pede um dia igual ou posterior a 10. O histórico continua com a última mudança no dia 10. |
| Conclusão | Opção 5, código 013, Concluída, dia 12. | A busca pelo código mostra abertura no dia 9 e atualizações nos dias 10 e 12. |
| Recálculo | Opção 9. | São 13 ocorrências. As 4 concluídas somam 17 dias. A média fica em 4,25 dias. |
| Persistência | Sair com 0, reabrir e consultar 013. | A descrição e o histórico completo de 013 são recuperados. A pilha exibe o evento do dia 12 no topo. |
| Atendimento pela fila | Opção 6, Examinar a primeira, dia 9. Abra a fila de novo. | 008 passa para Em análise. 009 ocupa a primeira posição. |

Nos testes de preparação, cópias temporárias também permitiram conferir código duplicado, situação desconhecida, falha de escrita, base vazia, campo com separador dentro do texto e conclusão no mesmo dia. Uma ocorrência aberta e concluída no mesmo dia, passando pela análise, conta como zero dias na média.
