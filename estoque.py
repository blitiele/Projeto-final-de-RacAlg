# ============================================================
#  Módulo de Estoque — Sistema de Revenda de Roupas
# ============================================================

estoque = {}  # { codigo: { nome, categoria, tamanho, preco, quantidade, vendidos } }


# ── Cadastrar produto ────────────────────────────────────────
def cadastrar_produto(codigo, nome, categoria, tamanho, preco, quantidade):
    """
    Cadastra um novo produto no estoque.

    Parâmetros:
        codigo (str)      — código único do produto
        nome (str)        — nome/descrição do produto
        categoria (str)   — ex: 'camiseta', 'calça', 'vestido'
        tamanho (str)     — ex: 'P', 'M', 'G', '38', '42'
        preco (float)     — preço de venda
        quantidade (int)  — quantidade inicial em estoque

    Retorna:
        str — mensagem de sucesso ou erro
    """
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


# ── Consultar estoque ────────────────────────────────────────
def consultar_estoque(codigo=None):
    """
    Consulta o estoque completo ou um produto específico.

    Parâmetros:
        codigo (str|None) — se informado, retorna apenas esse produto;
                            se None, retorna todos os produtos.

    Retorna:
        dict | list[dict] | str — dados do(s) produto(s) ou mensagem de erro
    """
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


# ── Atualizar quantidade ─────────────────────────────────────
def atualizar_quantidade(codigo, nova_quantidade):
    """
    Atualiza a quantidade em estoque de um produto.

    Parâmetros:
        codigo (str)         — código do produto
        nova_quantidade (int) — nova quantidade (substitui o valor atual)

    Retorna:
        str — mensagem de sucesso ou erro
    """
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


# ── Registrar venda ──────────────────────────────────────────
def registrar_venda(codigo, quantidade_vendida):
    """
    Registra a venda de um produto, reduzindo o estoque.

    Parâmetros:
        codigo (str)             — código do produto
        quantidade_vendida (int) — quantidade vendida

    Retorna:
        str — mensagem de sucesso ou erro
    """
    if codigo not in estoque:
        return f"Erro: produto com código '{codigo}' não encontrado."

    if quantidade_vendida <= 0:
        return "Erro: a quantidade vendida deve ser maior que zero."

    if estoque[codigo]["quantidade"] < quantidade_vendida:
        disponivel = estoque[codigo]["quantidade"]
        return (
            f"Erro: estoque insuficiente. "
            f"Disponível: {disponivel} unidade(s)."
        )

    estoque[codigo]["quantidade"] -= quantidade_vendida
    estoque[codigo]["vendidos"] += quantidade_vendida

    total = quantidade_vendida * estoque[codigo]["preco"]
    return (
        f"Venda registrada! {quantidade_vendida}x '{estoque[codigo]['nome']}' "
        f"— Total: R$ {total:.2f}. "
        f"Estoque restante: {estoque[codigo]['quantidade']} unidade(s)."
    )


# ── Produtos vendidos ────────────────────────────────────────
def relatorio_vendidos():
    """
    Exibe a quantidade de unidades vendidas por produto.

    Retorna:
        list[dict] — lista com código, nome e total vendido (ordenada por mais vendidos)
                     ou str se o estoque estiver vazio.
    """
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


# ── Remover produto ──────────────────────────────────────────
def remover_produto(codigo):
    """
    Remove um produto do estoque.

    Parâmetros:
        codigo (str) — código do produto a ser removido

    Retorna:
        str — mensagem de sucesso ou erro
    """
    if codigo not in estoque:
        return f"Erro: produto com código '{codigo}' não encontrado."

    nome = estoque.pop(codigo)["nome"]
    return f"Produto '{nome}' (cód. {codigo}) removido do estoque."


# ── Utilitário: exibir tabela no terminal ────────────────────
def exibir_estoque():
    """Imprime o estoque formatado no terminal."""
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


# ── Exemplo de uso ───────────────────────────────────────────
if __name__ == "__main__":
    # Cadastro
    print(cadastrar_produto("CAM001", "Camiseta Básica", "Camiseta", "M", 49.90, 30))
    print(cadastrar_produto("CAL002", "Calça Jeans",     "Calça",    "40", 129.90, 15))
    print(cadastrar_produto("VES003", "Vestido Floral",  "Vestido",  "P", 89.90, 10))

    # Consultar tudo
    exibir_estoque()

    # Vendas
    print(registrar_venda("CAM001", 5))
    print(registrar_venda("CAL002", 3))
    print(registrar_venda("VES003", 8))

    # Atualizar quantidade (reposição)
    print(atualizar_quantidade("VES003", 20))

    # Relatório de vendidos
    print("\n── Relatório de Vendidos ──")
    for item in relatorio_vendidos():
        print(f"  {item['nome']:20} — vendidos: {item['vendidos']:>4} | em estoque: {item['em_estoque']}")

    # Remover produto
    print(remover_produto("CAL002"))

    # Exibir estado final
    exibir_estoque()