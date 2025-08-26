import unittest

from fila import Fila
from Pilha import Pilha


class TestFila(unittest.TestCase):
    def test_operacoes_basicas_e_vazias(self):
        f = Fila()
        self.assertTrue(f.esta_vazia())
        self.assertIsNone(f.desenfileirar())
        self.assertIsNone(f.remover_ultimo())
        f.enfileirar(1)
        f.enfileirar(2)
        self.assertFalse(f.esta_vazia())
        self.assertEqual(str(f), str(f.itens))
        self.assertEqual(f.desenfileirar(), 1)
        self.assertEqual(f.remover_ultimo(), 2)
        self.assertTrue(f.esta_vazia())


class TestPilha(unittest.TestCase):
    def test_operacoes_basicas_e_vazia(self):
        p = Pilha()
        self.assertTrue(p.esta_vazia())
        self.assertIsNone(p.desempilhar())
        p.empilhar(1)
        p.empilhar(2)
        self.assertFalse(p.esta_vazia())
        self.assertEqual(p.desempilhar(), 2)
        self.assertEqual(p.desempilhar(), 1)
        self.assertTrue(p.esta_vazia())


if __name__ == "__main__":
    unittest.main()

