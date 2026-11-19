"""Dados e regras do painel comunitário Bairro em Dia."""

import csv
from pathlib import Path


PASTA_DADOS = Path(__file__).resolve().parent.parent / "dados"
CATEGORIAS = ["Iluminação", "Acessibilidade", "Limpeza", "Conservação"]
SITUACOES = ["Aberta", "Em análise", "Concluída"]
BAIRROS = ["Vila Ipê", "Jardim da Ponte"]
CAMPOS_CADASTRO = [
    "codigo", "categoria", "descricao", "bairro", "local", "dia_abertura", "status_inicial"
]
CAMPOS_EVENTO = ["codigo", "dia", "novo_status"]


def novo_painel():
    return {"ocorrencias": [], "por_codigo": {}, "fila": [], "historico": []}


def codigo_padrao(valor):
    digitos = valor.strip().lstrip("0")
    if digitos.isascii() and digitos.isdigit():
        return digitos.zfill(3)
    return ""


def proximo_codigo(painel):
    numero = 1
    while str(numero).zfill(3) in painel["por_codigo"]:
        numero += 1
    return str(numero).zfill(3)


def dia_simulado(valor):
    try:
        dia = int(valor)
    except (ValueError, TypeError):
        return 0
    return max(0, dia)


def ler_linhas(caminho, campos):
    with caminho.open(encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";", strict=True)
        if leitor.fieldnames != campos:
            raise ValueError(f"Confira o cabeçalho de {caminho.name}.")
        return list(leitor)


def gravar_linha(caminho, campos, linha):
    with caminho.open("a", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos, delimiter=";")
        escritor.writerow(linha)


def cadastrar(painel, linha, destino=None):
    codigo = codigo_padrao(linha["codigo"])
    categoria = linha["categoria"]
    descricao = linha["descricao"].strip()
    local = linha["local"].strip()
    dia = dia_simulado(linha["dia_abertura"])

    if not codigo:
        return "Use um código numérico maior que zero."
    elif codigo in painel["por_codigo"]:
        return "Código já cadastrado."
    elif not categoria:
        return "Categoria obrigatória."
    elif categoria not in CATEGORIAS:
        return "Categoria desconhecida."
    elif linha["bairro"] not in BAIRROS:
        return "Escolha um dos bairros da simulação."
    elif not descricao or not local:
        return "Descrição e local são obrigatórios."
    elif dia == 0:
        return "O dia de abertura precisa ser um inteiro maior que zero."
    elif linha["status_inicial"] != "Aberta":
        return "Toda ocorrência deve iniciar como Aberta."

    registro = {
        "codigo": codigo, "categoria": categoria, "descricao": descricao,
        "bairro": linha["bairro"], "local": local, "abertura": dia,
        "status": "Aberta", "ultimo_dia": dia
    }
    if destino is not None:
        gravar_linha(destino, CAMPOS_CADASTRO, linha)
    painel["ocorrencias"].append(registro)
    painel["por_codigo"][codigo] = registro
    painel["fila"].append(codigo)
    return ""


def atualizar(painel, linha, destino=None):
    codigo = codigo_padrao(linha["codigo"])
    dia = dia_simulado(linha["dia"])
    novo = linha["novo_status"]
    registro = painel["por_codigo"].get(codigo)

    if registro is None:
        return "Ocorrência não encontrada."
    atual = registro["status"]
    if novo not in SITUACOES:
        return "Situação desconhecida."
    elif atual == "Concluída":
        return "Esta ocorrência já está concluída."
    elif atual == novo:
        return "A ocorrência já está nessa situação."
    elif atual == "Aberta" and novo != "Em análise":
        return "Uma ocorrência aberta precisa passar por Em análise."
    elif atual == "Em análise" and novo != "Concluída":
        return "Uma ocorrência em análise só pode seguir para Concluída."
    elif dia < registro["ultimo_dia"]:
        return f"Use um dia inteiro igual ou posterior a {registro['ultimo_dia']}."

    if destino is not None:
        gravar_linha(destino, CAMPOS_EVENTO, linha)
    if atual == "Aberta":
        if painel["fila"][0] == codigo:
            painel["fila"].pop(0)
        else:
            painel["fila"].remove(codigo)
    registro["status"] = novo
    registro["ultimo_dia"] = dia
    painel["historico"].append({"codigo": codigo, "dia": dia, "antes": atual, "depois": novo})
    return ""


def carregar(pasta=PASTA_DADOS):
    painel = novo_painel()
    avisos = []
    fontes = [("ocorrencias.csv", CAMPOS_CADASTRO), ("historico.csv", CAMPOS_EVENTO)]
    for nome, campos in fontes:
        linhas = ler_linhas(pasta / nome, campos)
        for numero, linha in enumerate(linhas, start=2):
            if None in linha:
                erro = "Há colunas extras."
            else:
                for campo in campos:
                    linha[campo] = (linha[campo] or "").strip()
                if nome == "ocorrencias.csv":
                    erro = cadastrar(painel, linha)
                else:
                    erro = atualizar(painel, linha)
            if erro:
                codigo = linha["codigo"] or "sem código"
                avisos.append(f"{nome}, linha {numero} (código {codigo}) ignorada. {erro}")
    return painel, avisos


def filtrar(painel, categoria="", situacao=""):
    encontrados = []
    for registro in painel["ocorrencias"]:
        categoria_ok = not categoria or registro["categoria"] == categoria
        situacao_ok = not situacao or registro["status"] == situacao
        if categoria_ok and situacao_ok:
            encontrados.append(registro)
    return encontrados


def montar_hierarquia(painel):
    bairros = {}
    for registro in painel["ocorrencias"]:
        bairro = registro["bairro"]
        categoria = registro["categoria"]
        if bairro not in bairros:
            bairros[bairro] = {}
        if categoria not in bairros[bairro]:
            bairros[bairro][categoria] = []
        bairros[bairro][categoria].append(registro["codigo"])
    return bairros


def calcular_indicadores(painel):
    matriz = []
    for categoria in CATEGORIAS:
        matriz.append([0] * len(SITUACOES))
    por_situacao = [0] * len(SITUACOES)
    soma_dias = 0
    for registro in painel["ocorrencias"]:
        linha = CATEGORIAS.index(registro["categoria"])
        coluna = SITUACOES.index(registro["status"])
        matriz[linha][coluna] += 1
        por_situacao[coluna] += 1
        if registro["status"] == "Concluída":
            soma_dias += registro["ultimo_dia"] - registro["abertura"]
    return matriz, por_situacao, soma_dias
