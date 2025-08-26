import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from sistema import Sistema


def run_and_capture_output(func, *args, **kwargs):
    buf = io.StringIO()
    with redirect_stdout(buf):
        func(*args, **kwargs)
    return buf.getvalue()


class BaseIsolatedCwdTest(unittest.TestCase):
    def setUp(self):
        self._orig_cwd = os.getcwd()
        self._tmpdir = tempfile.TemporaryDirectory()
        os.chdir(self._tmpdir.name)

    def tearDown(self):
        os.chdir(self._orig_cwd)
        self._tmpdir.cleanup()


class TestSistemaErros(BaseIsolatedCwdTest):
    def test_cadastrar_cliente_duplicado_mostra_erro(self):
        s = Sistema()
        s.cadastrar_cliente(1, "Ana")
        out = run_and_capture_output(s.cadastrar_cliente, 1, "Ana")
        self.assertIn("Erro: já existe um cliente com o ID 1.", out)

    def test_remover_cliente_inexistente_mostra_mensagem(self):
        s = Sistema()
        out = run_and_capture_output(s.remover_cliente, 99)
        self.assertIn("Nenhum cliente encontrado com o ID 99.", out)

    def test_listar_clientes_sem_clientes(self):
        s = Sistema()
        out = run_and_capture_output(s.listar_clientes)
        self.assertIn("Nenhum cliente cadastrado.", out)

    def test_cadastrar_produto_id_duplicado(self):
        s = Sistema()
        s.cadastrar_produto(1, "Arroz", 10, 5.0)
        out = run_and_capture_output(s.cadastrar_produto, 1, "Feijao", 5, 4.0)
        self.assertIn("Erro: o ID 1 já está em uso", out)

    def test_cadastrar_produto_nome_duplicado_case_insensitive_whitespace(self):
        s = Sistema()
        s.cadastrar_produto(1, "  Arroz  Branco ", 10, 5.0)
        out = run_and_capture_output(s.cadastrar_produto, 2, "arroz   branco", 5, 4.0)
        self.assertIn("já está cadastrado", out)
        self.assertIn("opção 15", out)

    def test_cadastrar_produto_girafa_dispara_valueerror_mas_e_capturado(self):
        s = Sistema()
        out = run_and_capture_output(s.cadastrar_produto, 1, "girafa", 1, 1.0)
        self.assertIn("Não vendemos girafas!", out)

    def test_pesquisar_produto_nenhum_encontrado(self):
        s = Sistema()
        out = run_and_capture_output(s.pesquisar_produto, "inexistente")
        self.assertIn("Nenhum produto encontrado", out)

    def test_atualizar_quantidade_produto_inexistente(self):
        s = Sistema()
        out = run_and_capture_output(s.atualizar_quantidade_produto, 1, 10)
        self.assertIn("Nenhum produto encontrado com o ID 1.", out)

    def test_atualizar_quantidade_produto_quantidade_invalida(self):
        s = Sistema()
        s.cadastrar_produto(1, "Arroz", 10, 5.0)
        out = run_and_capture_output(s.atualizar_quantidade_produto, 1, 0)
        self.assertIn("maior que zero", out)

    def test_realizar_venda_erros_produto_cliente_estoque(self):
        s = Sistema()
        # Sem produto
        s.cadastrar_cliente(1, "Ana")
        out = run_and_capture_output(s.realizar_venda, 1, 1, 1)
        self.assertIn("Produto não encontrado.", out)

        # Sem cliente
        s = Sistema()
        s.cadastrar_produto(1, "Arroz", 1, 2.0)
        out = run_and_capture_output(s.realizar_venda, 1, 1, 1)
        self.assertIn("Cliente não encontrado.", out)

        # Estoque insuficiente
        s.cadastrar_cliente(2, "Bia")
        out = run_and_capture_output(s.realizar_venda, 2, 1, 5)
        self.assertIn("Estoque insuficiente.", out)

    def test_ver_fila_vendas_vazia(self):
        s = Sistema()
        out = run_and_capture_output(s.ver_fila_vendas)
        self.assertIn("Nenhuma venda registrada.", out)

    def test_desfazer_operacao_sem_itens(self):
        s = Sistema()
        out = run_and_capture_output(s.desfazer_operacao)
        self.assertIn("Nenhuma operação para desfazer.", out)

    def test_desfazer_operacao_de_venda_remove_da_fila_mais_recente(self):
        s = Sistema()
        s.cadastrar_cliente(1, "Ana")
        s.cadastrar_produto(1, "Arroz", 10, 1.0)
        s.realizar_venda(1, 1, 2)
        s.realizar_venda(1, 1, 1)
        # desfaz a última venda (1 unidade)
        s.desfazer_operacao()
        self.assertEqual(len(s.vendas.itens), 1)
        v = s.vendas.itens[0]
        self.assertEqual(v["quantidade"], 2)

    def test_desfazer_operacao_remove_venda_do_meio_da_fila(self):
        s = Sistema()
        s.cadastrar_cliente(1, "Ana")
        s.cadastrar_produto(1, "Arroz", 10, 1.0)
        # Três vendas distintas
        s.realizar_venda(1, 1, 1)  # A
        s.realizar_venda(1, 1, 2)  # B
        s.realizar_venda(1, 1, 3)  # C

        # Empilha manualmente uma operação de venda referente à venda do meio (B)
        venda_do_meio = list(s.vendas.itens)[1]
        s.operacoes.empilhar(("venda", venda_do_meio))

        # Ao desfazer, o sistema deve ser capaz de remover a venda B que não é a última da fila
        out = run_and_capture_output(s.desfazer_operacao)
        # Após remoção, devem restar duas vendas e nenhuma exceção deve ocorrer
        self.assertEqual(len(s.vendas.itens), 2)

    def test_valor_total_estoque_e_vendas(self):
        s = Sistema()
        s.cadastrar_cliente(1, "Ana")
        s.cadastrar_produto(1, "Arroz", 3, 10.0)
        s.cadastrar_produto(2, "Feijao", 2, 5.0)
        self.assertEqual(s.valor_total_estoque(), 3 * 10.0 + 2 * 5.0)
        s.realizar_venda(1, 1, 1)
        self.assertEqual(s.valor_total_vendas(), 10.0)

    def test_salvar_e_carregar_dados(self):
        # Cria um sistema, adiciona dados e salva
        s1 = Sistema()
        s1.cadastrar_cliente(1, "Ana")
        s1.cadastrar_produto(10, "Arroz", 2, 7.5)
        s1.realizar_venda(1, 10, 2)
        s1.salvar_dados()

        # Recarrega em outro objeto lendo os CSVs
        s2 = Sistema()
        self.assertEqual(len(s2.clientes), 1)
        self.assertEqual(len(s2.estoque), 1)
        self.assertFalse(s2.vendas.esta_vazia())
        self.assertGreater(s2.valor_total_vendas(), 0)


if __name__ == "__main__":
    unittest.main()

