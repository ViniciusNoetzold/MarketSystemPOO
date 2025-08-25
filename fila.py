class Fila:
    def __init__(self):
        self.itens = []

    def enfileirar(self, item):
        self.itens.append(item)

    def desenfileirar(self):
        return self.itens.pop(0) if self.itens else None

    def esta_vazia(self):
        return len(self.itens) == 0

    def __str__(self):
        return str(self.itens)