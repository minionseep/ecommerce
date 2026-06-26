

class ErroLoja(Exception):
    pass

class ProdutoNaoEncontrado(ErroLoja):
    pass


class EstoqueInsuficiente(ErroLoja):
    pass


class CupomInvalido(ErroLoja):
    pass


def criar_catalogo():
    return {}


def _chave(nome):
    return nome.strip().lower()


def adicionar_produto(catalogo, nome, preco, categoria, estoque):
    nome = nome.strip()
    if not nome:
        raise ValueError("Nome do produto não pode ser vazio.")
    if preco < 0:
        raise ValueError("Preço não pode ser negativo.")
    if estoque < 0:
        raise ValueError("Estoque não pode ser negativo.")

    catalogo[_chave(nome)] = {
        "nome": nome,
        "preco": float(preco),
        "categoria": categoria.strip().lower(),
        "estoque": int(estoque),
    }
    return catalogo[_chave(nome)]


def obter_produto(catalogo, nome):
    produto = catalogo.get(_chave(nome))
    if produto is None:
        raise ProdutoNaoEncontrado(f"Produto '{nome}' não existe no catálogo.")
    return produto


def buscar_por_nome(catalogo, termo):
    termo = termo.strip().lower()
    return [p for p in catalogo.values() if termo in p["nome"].lower()]


def buscar_por_categoria(catalogo, categoria):
    categoria = categoria.strip().lower()
    return [p for p in catalogo.values() if p["categoria"] == categoria]

def criar_carrinho():
    return {}


def adicionar_ao_carrinho(catalogo, carrinho, nome, quantidade=1):
    if quantidade <= 0:
        raise ValueError("Quantidade deve ser positiva.")

    produto = obter_produto(catalogo, nome)  # pode levantar ProdutoNaoEncontrado
    chave = _chave(nome)
    no_carrinho = carrinho.get(chave, 0)

    if no_carrinho + quantidade > produto["estoque"]:
        raise EstoqueInsuficiente(
            f"Estoque insuficiente de '{produto['nome']}': "
            f"disponível {produto['estoque']}, no carrinho {no_carrinho}, "
            f"pedido +{quantidade}."
        )

    carrinho[chave] = no_carrinho + quantidade
    return carrinho


def remover_do_carrinho(carrinho, nome, quantidade=None):
    chave = _chave(nome)
    if chave not in carrinho:
        raise ProdutoNaoEncontrado(f"'{nome}' não está no carrinho.")

    if quantidade is None or quantidade >= carrinho[chave]:
        del carrinho[chave]
    else:
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva.")
        carrinho[chave] -= quantidade
    return carrinho


def calcular_total(catalogo, carrinho):
    """Soma preço * quantidade de todos os itens do carrinho."""
    total = 0.0
    for chave, qtd in carrinho.items():
        total += catalogo[chave]["preco"] * qtd
    return round(total, 2)

CUPONS = {
    "BEMVINDO10": 10,
    "PROMO20": 20,
    "BLACK50": 50,
}


def aplicar_cupom(total, codigo, cupons=CUPONS):
    """Aplica um cupom percentual ao total. Retorna (total_com_desconto, valor_descontado).

    Levanta CupomInvalido se o código não existir.
    """
    codigo = codigo.strip().upper()
    if codigo not in cupons:
        raise CupomInvalido(f"Cupom '{codigo}' é inválido.")

    percentual = cupons[codigo]
    desconto = round(total * percentual / 100, 2)
    return round(total - desconto, 2), desconto



def finalizar_pedido(catalogo, carrinho, cupom=None):
    if not carrinho:
        raise ErroLoja("Carrinho vazio: não há o que finalizar.")

   
    for chave, qtd in carrinho.items():
        produto = catalogo[chave]
        if qtd > produto["estoque"]:
            raise EstoqueInsuficiente(
                f"'{produto['nome']}' ficou sem estoque suficiente "
                f"(pedido {qtd}, disponível {produto['estoque']})."
            )

  
    subtotal = calcular_total(catalogo, carrinho)
    desconto = 0.0
    total = subtotal
    if cupom:
        total, desconto = aplicar_cupom(subtotal, cupom)  
    itens = []
    for chave, qtd in carrinho.items():
        produto = catalogo[chave]
        produto["estoque"] -= qtd
        itens.append({
            "nome": produto["nome"],
            "quantidade": qtd,
            "preco_unitario": produto["preco"],
            "subtotal": round(produto["preco"] * qtd, 2),
        })

    resumo = {
        "itens": itens,
        "subtotal": subtotal,
        "cupom": cupom.strip().upper() if cupom else None,
        "desconto": desconto,
        "total": total,
    }

    carrinho.clear()  
    return resumo


def formatar_resumo(resumo):
    linhas = ["=" * 40, "RESUMO DO PEDIDO", "=" * 40]
    for item in resumo["itens"]:
        linhas.append(
            f"{item['quantidade']:>2}x {item['nome']:<20} "
            f"R$ {item['subtotal']:>8.2f}"
        )
    linhas.append("-" * 40)
    linhas.append(f"{'Subtotal:':<25} R$ {resumo['subtotal']:>8.2f}")
    if resumo["cupom"]:
        linhas.append(
            f"{'Cupom ' + resumo['cupom'] + ':':<25} -R$ {resumo['desconto']:>7.2f}"
        )
    linhas.append(f"{'TOTAL:':<25} R$ {resumo['total']:>8.2f}")
    linhas.append("=" * 40)
    return "\n".join(linhas)
