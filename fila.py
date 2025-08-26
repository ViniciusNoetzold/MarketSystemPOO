from collections import deque


class Fila:
    def __init__(self):
        self.itens = deque()

    def enfileirar(self, item):
        self.itens.append(item)

    def desenfileirar(self):
        return self.itens.popleft() if self.itens else None

    def remover_ultimo(self):
        return self.itens.pop() if self.itens else None

    def esta_vazia(self):
        return len(self.itens) == 0

    def __str__(self):
        return str(self.itens)