from fila import Fila
from Pilha import Pilha
from produto import Produto
from clientes import Cliente
import csv
import os

class Sistema:
    
    def __init__(self):
        self.estoque = []
        self.clientes = []
        self.vendas = Fila()
        self.operacoes = Pilha()
        self.total_vendas = 0.0
        self.carregar_dados()

    def cadastrar_cliente(self, id, nome):
        for c in self.clientes:
            if c.id == id:
                print(f"Erro: já existe um cliente com o ID {id}.")
                return
        cliente = Cliente(id, nome)
        self.clientes.append(cliente)
        self.operacoes.empilhar(("cadastro_cliente", cliente))
        print("Cliente cadastrado com sucesso!")

    def remover_clientes_duplicados(self):
        ids_vistos = set()
        unicos = []
        removidos = 0
        for c in self.clientes:
            if c.id in ids_vistos:
                removidos += 1
            else:
                ids_vistos.add(c.id)
                unicos.append(c)
        self.clientes = unicos
        if removidos:
            print(f"{removidos} cliente(s) duplicado(s) removido(s) por ID.")
        else:
            print("Nenhum cliente duplicado encontrado.")

    def remover_cliente(self, id):
        cliente = next((c for c in self.clientes if c.id == id), None)
        if cliente:
            self.clientes.remove(cliente)
            self.operacoes.empilhar(("remover_cliente", cliente))
            print(f"Cliente {cliente.nome} removido com sucesso.")
        else:
            print(f"Nenhum cliente encontrado com o ID {id}.")

    def listar_clientes(self):
        if not self.clientes:
            print("Nenhum cliente cadastrado.")
        else:
            for c in self.clientes:
                print(c)

    def cadastrar_produto(self, id, nome, quantidade, preco):
        try:
            def _norm(s: str) -> str:
                return " ".join(s.strip().lower().split())

            nome_norm = _norm(nome)

            for produto in self.estoque:
                if produto.id == id:
                    print(f"Erro: o ID {id} já está em uso pelo produto '{produto.nome}'.")
                    return
            for produto in self.estoque:
                if _norm(produto.nome) == nome_norm:
                    print(f"Erro: o produto '{produto.nome}' já está cadastrado. "
                    f"Use a opção 15 do menu para atualizar a quantidade/preço.")
                    return

            produto = Produto(id, nome, quantidade, preco)
            self.estoque.append(produto)
            self.operacoes.empilhar(("cadastro_produto", produto))
            print("Produto cadastrado com sucesso!")
    
        except ValueError as e:
            print(e)

    def listar_produtos(self):
        if not self.estoque:
            print("Nenhum produto no estoque.")
        else:
            for p in self.estoque:
                print(p)

    def pesquisar_produto(self, termo):
        termo = termo.strip().lower()
        encontrados = []

        for p in self.estoque:
            if termo.isdigit() and str(p.id) == termo:
                encontrados.append(p)
            elif termo in p.nome.lower():
                encontrados.append(p)

        if encontrados:
            print("Produtos encontrados:")
            for p in encontrados:
                print(p)
        else:
            print("Nenhum produto encontrado com esse termo.")

    def atualizar_quantidade_produto(self, id, quantidade):
        produto = next((p for p in self.estoque if p.id == id), None)
        if produto:
            if quantidade > 0:
                produto.quantidade += quantidade
                self.operacoes.empilhar(("atualizar_quantidade", (produto, quantidade)))
                print(f"Quantidade do produto '{produto.nome}' atualizada. Novo total: {produto.quantidade}")
            else:
                print("A quantidade adicionada deve ser maior que zero.")
        else:
            print(f"Nenhum produto encontrado com o ID {id}.")

    def realizar_venda(self, cliente_id, produto_id, quantidade):
        produto = next((p for p in self.estoque if p.id == produto_id), None)
        cliente = next((c for c in self.clientes if c.id == cliente_id), None)

        if not produto:
            print("Produto não encontrado.")
            return
        if not cliente:
            print("Cliente não encontrado.")
            return
        if quantidade > produto.quantidade:
            print("Estoque insuficiente.")
            return

        valor_total = quantidade * produto.preco
        produto.quantidade -= quantidade
        cliente.adicionar_gasto(valor_total)
        self.total_vendas += valor_total

        venda = {
            "produto": produto.nome,
            "quantidade": quantidade,
            "valor": valor_total,
            "cliente": cliente.nome
        }
        self.vendas.enfileirar(venda)
        self.operacoes.empilhar(("venda", venda))

        print(f"Venda realizada com sucesso! (Valor total: R${valor_total:.2f})")

    def ver_fila_vendas(self):
        if self.vendas.esta_vazia():
            print("Nenhuma venda registrada.")
        else:
            for v in self.vendas.itens:
                print(v)

    def desfazer_operacao(self):
        if self.operacoes.esta_vazia():
            print("Nenhuma operação para desfazer.")
            return

        operacao, item = self.operacoes.desempilhar()

        if operacao == "cadastro_produto":
            self.estoque.remove(item)
            print(f"Cadastro do produto {item.nome} desfeito.")
        elif operacao == "cadastro_cliente":
            self.clientes.remove(item)
            print(f"Cadastro do cliente {item.nome} desfeito.")
        elif operacao == "remover_cliente":
            self.clientes.append(item)
            print(f"Remoção do cliente {item.nome} desfeita.")
        elif operacao == "venda":
            produto = next((p for p in self.estoque if p.nome == item["produto"]), None)
            cliente = next((c for c in self.clientes if c.nome == item["cliente"]), None)
            if produto and cliente:
                produto.quantidade += item["quantidade"]
                cliente.total_gasto -= item["valor"]
                self.total_vendas -= item["valor"]
                # Remove a venda correspondente da fila, priorizando a mais recente
                if self.vendas.itens:
                    if self.vendas.itens[-1] == item:
                        self.vendas.itens.pop()
                    else:
                        # Remove a ocorrência mais recente do item na deque
                        try:
                            self.vendas.itens.reverse()
                            self.vendas.itens.remove(item)
                            self.vendas.itens.reverse()
                        except ValueError:
                            pass
                print(f"Venda do produto {item['produto']} desfeita.")
        elif operacao == "atualizar_quantidade":
            produto, quantidade = item
            produto.quantidade -= quantidade
            print(f"Atualização de quantidade do produto {produto.nome} desfeita.")

    def valor_total_estoque(self):
        return sum(p.quantidade * p.preco for p in self.estoque)

    def valor_total_vendas(self):
        return self.total_vendas

    def clientes_totais(self):
        for c in self.clientes:
            print(c)

    def salvar_dados(self):
        with open("clientes.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "nome", "total_gasto"])
            for c in self.clientes:
                writer.writerow([c.id, c.nome, c.total_gasto])
        with open("produtos.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "nome", "quantidade", "preco"])
            for p in self.estoque:
                writer.writerow([p.id, p.nome, p.quantidade, p.preco])
        with open("vendas.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["cliente", "produto", "quantidade", "valor"])
            for v in self.vendas.itens:
                writer.writerow([v["cliente"], v["produto"], v["quantidade"], v["valor"]])

        print("Dados salvos com sucesso!")
    
    def carregar_dados(self):
        if os.path.exists("clientes.csv"):
            with open("clientes.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cliente = Cliente(int(row["id"]), row["nome"])
                    cliente.total_gasto = float(row["total_gasto"])
                    self.clientes.append(cliente)
        if os.path.exists("produtos.csv"):
            with open("produtos.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    produto = Produto(int(row["id"]), row["nome"], int(row["quantidade"]), float(row["preco"]))
                    self.estoque.append(produto)
        if os.path.exists("vendas.csv"):
            with open("vendas.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    venda = {
                        "cliente": row["cliente"],
                        "produto": row["produto"],
                        "quantidade": int(row["quantidade"]),
                        "valor": float(row["valor"])
                    }
                    self.vendas.enfileirar(venda)
                    self.total_vendas += venda["valor"]

        print("Dados carregados com sucesso!")