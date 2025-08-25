class Cliente:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
        self.total_gasto = 0.0

    def adicionar_gasto(self, valor):
        self.total_gasto += valor

    def __str__(self):
        return f"ID: {self.id} | Nome: {self.nome} | Total gasto: R${self.total_gasto:.2f}"