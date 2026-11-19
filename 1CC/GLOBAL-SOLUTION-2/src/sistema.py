"""Menu de terminal do projeto Bairro em Dia. Execute com python src/sistema.py."""

import csv
import ocorrencias as dados


MENU = """
1  Listar ocorrências
2  Cadastrar ocorrência
3  Buscar por código
4  Filtrar ocorrências
5  Atualizar situação
6  Fila de triagem
7  Histórico recente
8  Bairros e categorias
9  Indicadores
0  Sair"""


def escolher(titulo, opcoes, todos=False):
    print(titulo)
    for numero, opcao in enumerate(opcoes, start=1):
        print(f"  {numero}  {opcao}")
    if todos:
        print("  0  Todas")
    while True:
        entrada = input("Escolha o número > ").strip()
        if todos and entrada == "0":
            return ""
        for numero, opcao in enumerate(opcoes, start=1):
            if entrada == str(numero):
                return opcao
        print("Opção inválida. Digite um dos números da lista.")


def listar(registros):
    if not registros:
        print("Nenhuma ocorrência encontrada.")
        return
    print("Código | Categoria      | Situação   | Bairro e local")
    for r in registros:
        print(f"{r['codigo']:>6} | {r['categoria']:<14} | {r['status']:<10} | "
              f"{r['bairro']} / {r['local']}")


def novo_cadastro(painel):
    print("Use uma descrição breve e um local público genérico. Evite dados pessoais.")
    categoria = escolher("Categoria", dados.CATEGORIAS)
    bairro = escolher("Bairro", dados.BAIRROS)
    local = input("Local genérico > ").strip()
    descricao = input("Descrição > ").strip()
    dia = input("Dia simulado de abertura (1, 2, 3...) > ").strip()
    codigo = dados.proximo_codigo(painel)
    linha = {
        "codigo": codigo, "categoria": categoria, "descricao": descricao,
        "bairro": bairro, "local": local, "dia_abertura": dia, "status_inicial": "Aberta"
    }
    erro = dados.cadastrar(painel, linha, dados.PASTA_DADOS / "ocorrencias.csv")
    print(erro or f"Ocorrência {codigo} cadastrada. Situação atual: Aberta.")


def buscar(painel):
    codigo = dados.codigo_padrao(input("Código da ocorrência > "))
    r = painel["por_codigo"].get(codigo)
    if r is None:
        print("Ocorrência não encontrada.")
        return
    listar([r])
    print(f"Descrição: {r['descricao']}")
    print(f"Dia {r['abertura']} | Abertura")
    for evento in painel["historico"]:
        if evento["codigo"] == codigo:
            print(f"Dia {evento['dia']} | {evento['antes']} → {evento['depois']}")


def consultar_filtros(painel):
    categoria = escolher("Filtrar por categoria", dados.CATEGORIAS, todos=True)
    situacao = escolher("Filtrar por situação", dados.SITUACOES, todos=True)
    listar(dados.filtrar(painel, categoria, situacao))


def mudar_situacao(painel, codigo, nova):
    dia = input("Dia simulado da atualização > ").strip()
    linha = {"codigo": codigo, "dia": dia, "novo_status": nova}
    erro = dados.atualizar(painel, linha, dados.PASTA_DADOS / "historico.csv")
    print(erro or f"Ocorrência {codigo} atualizada para {nova}.")


def atualizar_por_codigo(painel):
    codigo = dados.codigo_padrao(input("Código da ocorrência > "))
    r = painel["por_codigo"].get(codigo)
    if r is None:
        print("Ocorrência não encontrada.")
    elif r["status"] == "Concluída":
        print("Esta ocorrência já está concluída.")
    else:
        print(f"Situação atual: {r['status']}. Último registro no dia {r['ultimo_dia']}.")
        nova = escolher("Nova situação", dados.SITUACOES)
        mudar_situacao(painel, codigo, nova)


def mostrar_fila(painel):
    fila = painel["fila"]
    if not fila:
        print("Fila vazia. Todas as ocorrências já passaram pela triagem.")
        return
    print("Fila de triagem em ordem de cadastro")
    for posicao, codigo in enumerate(fila, start=1):
        r = painel["por_codigo"][codigo]
        print(f"{posicao}. {codigo} | {r['categoria']} | {r['local']}")
    escolha = escolher("Ação da fila", ["Examinar a primeira", "Voltar"])
    if escolha == "Examinar a primeira":
        mudar_situacao(painel, fila[0], "Em análise")


def mostrar_historico(painel):
    print("Histórico de atualizações, da mais recente à mais antiga")
    if not painel["historico"]:
        print("Nenhuma atualização registrada.")
    for evento in reversed(painel["historico"]):
        print(f"Dia {evento['dia']} | {evento['codigo']} | {evento['antes']} → {evento['depois']}")


def mostrar_hierarquia(painel):
    bairros = dados.montar_hierarquia(painel)
    if not bairros:
        print("Nenhum bairro com ocorrências.")
    for bairro, categorias in bairros.items():
        print(bairro)
        for categoria, codigos in categorias.items():
            print(f"  {categoria} | {', '.join(codigos)}")


def decimal(valor, casas):
    return f"{valor:.{casas}f}".replace(".", ",")


def exibir_indicadores(painel):
    total = len(painel["ocorrencias"])
    if not total:
        print("Nenhuma ocorrência válida para calcular indicadores.")
        return
    matriz, por_situacao, soma_dias = dados.calcular_indicadores(painel)
    print(f"Base: {total} ocorrências válidas. Percentuais sobre o total.")
    print("Categoria      | Aberta | Em análise | Concluída | Total | Parcela")
    pendencias = []
    for categoria, linha in zip(dados.CATEGORIAS, matriz):
        abertas, em_analise, concluidas = linha
        subtotal = sum(linha)
        parcela = decimal(100 * subtotal / total, 1)
        print(f"{categoria:<14} | {abertas:>6} | {em_analise:>10} | "
              f"{concluidas:>9} | {subtotal:>5} | {parcela:>5}%")
        pendencias.append(abertas + em_analise)
    print("Por situação")
    for situacao, quantidade in zip(dados.SITUACOES, por_situacao):
        print(f"  {situacao}: {quantidade} ({decimal(100 * quantidade / total, 1)}%)")
    abertas, em_analise, concluidas = por_situacao
    print(f"Pendências (abertas + em análise): {abertas} + {em_analise} = {abertas + em_analise}")
    if concluidas:
        media = decimal(soma_dias / concluidas, 2)
        print(f"Tempo médio até conclusão: {soma_dias} dias / {concluidas} concluídas = {media} dias.")
    else:
        print("Tempo médio indisponível. Ainda não há ocorrências concluídas.")

    maior = max(pendencias)
    if maior:
        destaques = []
        for categoria, quantidade in zip(dados.CATEGORIAS, pendencias):
            if quantidade == maior:
                destaques.append(categoria)
        print(f"Maior número de pendências por categoria ({maior}): {', '.join(destaques)}.")
    else:
        print("Todas as ocorrências cadastradas estão concluídas.")


def main():
    try:
        painel, avisos = dados.carregar()
    except (OSError, ValueError, csv.Error) as erro:
        print(f"Falha ao ler os dados. Confira os arquivos em dados/. Detalhe: {erro}")
        return
    print("BAIRRO EM DIA | Painel comunitário simulado")
    for aviso in avisos:
        print(aviso)
    print(f"{len(painel['ocorrencias'])} ocorrências válidas | {len(painel['historico'])} atualizações")
    while True:
        print(MENU)
        opcao = input("Opção do menu > ").strip()
        try:
            if opcao == "0":
                print("Sessão encerrada.")
                break
            elif opcao == "1":
                listar(painel["ocorrencias"])
            elif opcao == "2":
                novo_cadastro(painel)
            elif opcao == "3":
                buscar(painel)
            elif opcao == "4":
                consultar_filtros(painel)
            elif opcao == "5":
                atualizar_por_codigo(painel)
            elif opcao == "6":
                mostrar_fila(painel)
            elif opcao == "7":
                mostrar_historico(painel)
            elif opcao == "8":
                mostrar_hierarquia(painel)
            elif opcao == "9":
                exibir_indicadores(painel)
            else:
                print("Opção inválida. Escolha um número do menu.")
        except OSError as erro:
            print(f"Falha ao gravar. Confira a permissão de escrita na pasta dados/. Detalhe: {erro}")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nSessão encerrada.")
