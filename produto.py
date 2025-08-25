class Produto:
    def __init__(self, id, nome, quantidade, preco):
        if nome.lower() == "girafa":
            raise ValueError("Não vendemos girafas!")
        
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def __str__(self):
        return f"ID: {self.id} | Nome: {self.nome} | Quantidade: {self.quantidade} | Preço: R${self.preco:.2f}"