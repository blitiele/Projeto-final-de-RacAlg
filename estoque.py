estoque = {}  # { codigo: { nome, categoria, tamanho, preco, quantidade, vendidos } }

def cadastrar_produto(codigo, nome, categoria, tamanho, preco, quantidade):
    if codigo in estoque:
        return f"Erro: produto com código '{codigo}' já existe. Use atualizar_quantidade() para alterar o estoque."
    if preco < 0 or quantidade < 0:
        return "Erro: preço e quantidade não podem ser negativos."
    estoque[codigo] = {
        "nome": nome,
        "categoria": categoria,
        "tamanho": tamanho,
        "preco": float(preco),
        "quantidade": int(quantidade),
        "vendidos": 0,
    }
    return f"Produto '{nome}' (cód. {codigo}) cadastrado com sucesso!"

def consultar_estoque(codigo=None):
    if not estoque:
        return "Estoque vazio."
    if codigo:
        if codigo not in estoque:
            return f"Erro: produto com código '{codigo}' não encontrado."
        produto = estoque[codigo].copy()
        produto["codigo"] = codigo
        return produto
    resultado = []
    for cod, dados in estoque.items():
        item = dados.copy()
        item["codigo"] = cod
        resultado.append(item)
    return resultado

def atualizar_quantidade(codigo, nova_quantidade):
    if codigo not in estoque:
        return f"Erro: produto com código '{codigo}' não encontrado."
    if nova_quantidade < 0:
        return "Erro: quantidade não pode ser negativa."
    anterior = estoque[codigo]["quantidade"]
    estoque[codigo]["quantidade"] = int(nova_quantidade)
    return (
        f"Quantidade do produto '{estoque[codigo]['nome']}' atualizada: "
        f"{anterior} → {nova_quantidade}."
    )

def registrar_venda(codigo, quantidade_vendida):
    if codigo not in estoque:
        return f"Erro: produto com código '{codigo}' não encontrado."
    if quantidade_vendida <= 0:
        return "Erro: a quantidade vendida deve ser maior que zero."
    if estoque[codigo]["quantidade"] < quantidade_vendida:
        disponivel = estoque[codigo]["quantidade"]
        return f"Erro: estoque insuficiente. Disponível: {disponivel} unidade(s)."
    estoque[codigo]["quantidade"] -= quantidade_vendida
    estoque[codigo]["vendidos"] += quantidade_vendida
    total = quantidade_vendida * estoque[codigo]["preco"]
    return (
        f"Venda registrada! {quantidade_vendida}x '{estoque[codigo]['nome']}' "
        f"— Total: R$ {total:.2f}. "
        f"Estoque restante: {estoque[codigo]['quantidade']} unidade(s)."
    )

def relatorio_vendidos():
    if not estoque:
        return "Estoque vazio."
    relatorio = [
        {
            "codigo": cod,
            "nome": dados["nome"],
            "categoria": dados["categoria"],
            "tamanho": dados["tamanho"],
            "preco": dados["preco"],
            "vendidos": dados["vendidos"],
            "em_estoque": dados["quantidade"],
        }
        for cod, dados in estoque.items()
    ]
    relatorio.sort(key=lambda x: x["vendidos"], reverse=True)
    return relatorio

def remover_produto(codigo):
    if codigo not in estoque:
        return f"Erro: produto com código '{codigo}' não encontrado."
    nome = estoque.pop(codigo)["nome"]
    return f"Produto '{nome}' (cód. {codigo}) removido do estoque."

def exibir_estoque():
    dados = consultar_estoque()
    if isinstance(dados, str):
        print(dados)
        return
    print(f"\n{'─'*70}")
    print(f"{'CÓD.':<8} {'NOME':<20} {'CAT.':<12} {'TAM.':<6} "
          f"{'PREÇO':>8} {'ESTOQUE':>8} {'VENDIDOS':>9}")
    print(f"{'─'*70}")
    for p in dados:
        print(
            f"{p['codigo']:<8} {p['nome']:<20} {p['categoria']:<12} "
            f"{p['tamanho']:<6} R${p['preco']:>7.2f} "
            f"{p['quantidade']:>8} {p['vendidos']:>9}"
        )
    print(f"{'─'*70}\n")

def _input_float(mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("  Digite um número válido.")

def _input_int(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("  Digite um número inteiro válido.")

def _pausar():
    input("\nPressione Enter para continuar...")

def menu():
    """Inicia o menu interativo para a autônoma gerenciar o estoque."""

    _carregar_revendedora()

    opcoes = {
        "1": ("Visualizar estoque",         _menu_visualizar),
        "2": ("Cadastrar produto",           _menu_cadastrar),
        "3": ("Atualizar quantidade",        _menu_atualizar),
        "4": ("Registrar venda",             _menu_venda),
        "5": ("Remover produto",             _menu_remover),
        "6": ("Relatório de vendidos",       _menu_relatorio),
        "0": ("Sair",                        None),
    }

    while True:
        print("\n" + "═"*40)
        print("   SISTEMA DE ESTOQUE — REVENDA DE ROUPAS")
        print("═"*40)
        for chave, (descricao, _) in opcoes.items():
            print(f"  [{chave}] {descricao}")
        print("═"*40)

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            print("\nAté mais!\n")
            break
        elif escolha in opcoes:
            opcoes[escolha][1]()
        else:
            print("Opção inválida. Tente novamente.")


def _menu_visualizar():
    print("\n── Estoque atual ──")
    exibir_estoque()
    _pausar()


def _menu_cadastrar():
    print("\n── Cadastrar novo produto ──")
    codigo    = input("Código do produto : ").strip().upper()
    nome      = input("Nome              : ").strip()
    categoria = input("Categoria         : ").strip()
    tamanho   = input("Tamanho           : ").strip().upper()
    preco     = _input_float("Preço (R$)        : ")
    quantidade = _input_int("Quantidade inicial: ")
    print(cadastrar_produto(codigo, nome, categoria, tamanho, preco, quantidade))
    _pausar()


def _menu_atualizar():
    print("\n── Atualizar quantidade ──")
    exibir_estoque()
    codigo        = input("Código do produto    : ").strip().upper()
    nova_qtd      = _input_int("Nova quantidade      : ")
    print(atualizar_quantidade(codigo, nova_qtd))
    _pausar()


def _menu_venda():
    print("\n── Registrar venda ──")
    exibir_estoque()
    codigo    = input("Código do produto  : ").strip().upper()
    quantidade = _input_int("Quantidade vendida : ")
    print(registrar_venda(codigo, quantidade))
    _pausar()


def _menu_remover():
    print("\n── Remover produto ──")
    exibir_estoque()
    codigo = input("Código do produto a remover: ").strip().upper()
    confirmacao = input(f"Confirmar remoção de '{codigo}'? (s/n): ").strip().lower()
    if confirmacao == "s":
        print(remover_produto(codigo))
    else:
        print("Operação cancelada.")
    _pausar()


def _menu_relatorio():
    print("\n── Relatório de Vendidos ──")
    dados = relatorio_vendidos()
    if isinstance(dados, str):
        print(dados)
    else:
        print(f"\n{'─'*60}")
        print(f"{'NOME':<22} {'CAT.':<12} {'TAM.':<6} {'VENDIDOS':>9} {'ESTOQUE':>8}")
        print(f"{'─'*60}")
        for item in dados:
            print(
                f"{item['nome']:<22} {item['categoria']:<12} {item['tamanho']:<6} "
                f"{item['vendidos']:>9} {item['em_estoque']:>8}"
            )
        print(f"{'─'*60}")
    _pausar()

def _carregar_revendedora():
    """Carrega o catálogo inicial da revendedora fictícia."""
    produtos = [
        ("CAM001", "Camiseta Básica",    "Camiseta", "P",  29.90, 20),
        ("CAM002", "Camiseta Listrada",  "Camiseta", "M",  34.90, 15),
        ("CAM003", "Camiseta Polo",      "Camiseta", "G",  59.90, 10),
        ("CAL001", "Calça Jeans Skinny", "Calça",    "38", 119.90, 12),
        ("CAL002", "Calça Jeans Wide",   "Calça",    "40", 129.90,  8),
        ("CAL003", "Calça Moletom",      "Calça",    "M",   79.90, 10),
        ("VES001", "Vestido Floral",     "Vestido",  "P",   89.90,  7),
        ("VES002", "Vestido Midi",       "Vestido",  "M",   99.90,  5),
        ("BLU001", "Blusa de Frio",      "Blusa",    "G",   69.90, 14),
        ("SHO001", "Shorts Jeans",       "Short",    "38",  49.90, 18),
    ]
    for args in produtos:
        cadastrar_produto(*args)
    print(" Catálogo da revendedora carregado com 10 produtos.")

if _name_ == "_main_":
    menu()