class Pilha:
    def __init__(self):
        self.itens = []

    def empilhar(self, item):
        self.itens.append(item)

    def desempilhar(self):
        return self.itens.pop() if self.itens else None

    def esta_vazia(self):
        return len(self.itens) == 0

    def __str__(self):
        return str(self.itens)