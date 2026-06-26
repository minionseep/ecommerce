
import loja

def main():
    
    catalogo = loja.criar_catalogo()
    loja.adicionar_produto(catalogo, "Teclado Mecânico", 250.00, "Periféricos", estoque=5)
    loja.adicionar_produto(catalogo, "Mouse Gamer", 150.00, "Periféricos", estoque=3)
    loja.adicionar_produto(catalogo, "Monitor 24\"", 900.00, "Monitores", estoque=2)
    loja.adicionar_produto(catalogo, "Cadeira Gamer", 1200.00, "Móveis", estoque=1)

    print(">> Busca por nome 'gamer':")
    for p in loja.buscar_por_nome(catalogo, "gamer"):
        print(f"   - {p['nome']} (R$ {p['preco']:.2f})")

    print("\n>> Busca por categoria 'Periféricos':")
    for p in loja.buscar_por_categoria(catalogo, "Periféricos"):
        print(f"   - {p['nome']} ({p['estoque']} em estoque)")
        
    carrinho = loja.criar_carrinho()
    loja.adicionar_ao_carrinho(catalogo, carrinho, "Teclado Mecânico", 2)
    loja.adicionar_ao_carrinho(catalogo, carrinho, "Mouse Gamer", 1)
    loja.adicionar_ao_carrinho(catalogo, carrinho, "Monitor 24\"", 1)

    print(f"\n>> Total do carrinho: R$ {loja.calcular_total(catalogo, carrinho):.2f}")

    print("\n>> Tentando comprar 10 mouses (só há 3):")
    try:
        loja.adicionar_ao_carrinho(catalogo, carrinho, "Mouse Gamer", 10)
    except loja.EstoqueInsuficiente as e:
        print(f"   [ERRO] {e}")

    print("\n>> Tentando finalizar com cupom inválido:")
    try:
        loja.finalizar_pedido(catalogo, dict(carrinho), cupom="NAOEXISTE")
    except loja.CupomInvalido as e:
        print(f"   [ERRO] {e}")

 
    print("\n>> Finalizando com cupom PROMO20:")
    resumo = loja.finalizar_pedido(catalogo, carrinho, cupom="PROMO20")
    print(loja.formatar_resumo(resumo))

    print("\n>> Estoque após o pedido:")
    teclado = loja.obter_produto(catalogo, "Teclado Mecânico")
    print(f"   - {teclado['nome']}: {teclado['estoque']} unidades restantes")


if __name__ == "__main__":
    main()
