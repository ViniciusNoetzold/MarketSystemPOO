from sistema import Sistema
import os
os.system("color 3")

sistema = Sistema()

def ler_inteiro(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor.isdigit():
            return int(valor)
        else:
            print("Por favor digite corretamente.")

def ler_float(mensagem):
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            print("Por favor digite corretamente.")

def ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor.replace(" ", "").isalpha():
            return valor
        else:
            print("Por favor digite corretamente.")

while True:
    print("\n===== MENU ESTOQUE =====")
    print("1 - Cadastrar cliente")
    print("2 - Listar clientes")
    print("3 - Cadastrar produto")
    print("4 - Listar produtos")
    print("5 - Realizar venda")
    print("6 - Ver fila de vendas")
    print("7 - Desfazer última operação")
    print("8 - Exibir valor total do estoque")
    print("9 - Exibir valor total de vendas realizadas")
    print("10 - Exibir clientes e valores totais gastos")
    print("11 - Sair")
    print("12 - Salvar Dados")
    print("13 - Remover cliente por ID")
    print("14 - Pesquisar produto por nome ou ID")
    print("15 - Atualizar quantidade de produto existente")
    print("========================")
    

    opcao = input("Escolha: ")

    if opcao == "1":
        id = ler_inteiro("ID do cliente: ")
        nome = ler_texto("Nome do cliente: ")
        sistema.cadastrar_cliente(id, nome)

    elif opcao == "2":
        sistema.listar_clientes()

    elif opcao == "3":
        id = ler_inteiro("ID do produto: ")
        nome = ler_texto("Nome do produto: ")
        quantidade = ler_inteiro("Quantidade: ")
        preco = ler_float("Preço: ")
        sistema.cadastrar_produto(id, nome, quantidade, preco)

    elif opcao == "4":
        sistema.listar_produtos()

    elif opcao == "5":
        cliente_id = ler_inteiro("ID do cliente: ")
        produto_id = ler_inteiro("ID do produto: ")
        quantidade = ler_inteiro("Quantidade: ")
        sistema.realizar_venda(cliente_id, produto_id, quantidade)

    elif opcao == "6":
        sistema.ver_fila_vendas()

    elif opcao == "7":
        sistema.desfazer_operacao()

    elif opcao == "8":
        print(f"Valor total do estoque: R${sistema.valor_total_estoque():.2f}")

    elif opcao == "9":
        print(f"Valor total de vendas: R${sistema.valor_total_vendas():.2f}")

    elif opcao == "10":
        sistema.clientes_totais()

    elif opcao == "11":
        sistema.salvar_dados()
        print("Saindo do sistema... Até logo!")
        os.system("color 2")
        break

    elif opcao == "12":
        sistema.salvar_dados()

    elif opcao == "13":
        id = ler_inteiro("ID do cliente a remover: ")
        sistema.remover_cliente(id)

    elif opcao == "14":
        termo = input("Digite o ID ou parte do nome do produto: ")
        sistema.pesquisar_produto(termo)

    elif opcao == "15":
        id = ler_inteiro("ID do produto a atualizar: ")
        quantidade = ler_inteiro("Quantidade a adicionar: ")
        sistema.atualizar_quantidade_produto(id, quantidade)

    else:
        print("Opção inválida.")