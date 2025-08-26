## Sistema de Estoque e Vendas (CLI em Python)

Aplicação de terminal para cadastro de clientes e produtos, realização de vendas, visualização de fila de vendas e desfazer operações. Os dados são persistidos em arquivos CSV.

### Tecnologias
- **Linguagem**: Python 3 (sem dependências externas)
- **Persistência**: Arquivos CSV (`clientes.csv`, `produtos.csv`, `vendas.csv`)
- **Estruturas de dados**: `deque` (fila) e lista como pilha para desfazer

### Estrutura do projeto
- `main.py`: ponto de entrada com menu interativo.
- `sistema.py`: regra de negócio (estoque, clientes, vendas, desfazer, salvar/carregar CSV).
- `clientes.py`: classe `Cliente`.
- `produto.py`: classe `Produto`.
- `fila.py`: implementação de fila (baseada em `collections.deque`).
- `Pilha.py`: implementação de pilha (lista).
- `clientes.csv` | `produtos.csv` | `vendas.csv`: dados persistidos (criados/atualizados pelo sistema).

### Requisitos
- Python 3.8 ou superior
- Sistema operacional: Linux, macOS ou Windows

Observação: o comando de cor usado em `main.py` (`os.system("color 3")`) é específico do Windows. Em outros sistemas, ele é ignorado sem impactar o funcionamento.

### Como executar
1. Abra um terminal na pasta do projeto.
2. Execute:

```bash
python3 main.py
```

3. Siga as opções do menu.

### Funcionalidades (menu)
- **1 - Cadastrar cliente**: cria um cliente com `ID` e `Nome` (IDs não podem repetir).
- **2 - Listar clientes**: exibe todos os clientes cadastrados.
- **3 - Cadastrar produto**: cria produto com `ID`, `Nome`, `Quantidade` e `Preço`.
  - Regras: `ID` único; nomes iguais (ignorando maiúsc./minúsc. e espaços) não são permitidos; não é permitido nome "girafa".
- **4 - Listar produtos**: exibe o estoque.
- **5 - Realizar venda**: informa `ID do cliente`, `ID do produto` e `Quantidade`.
  - Atualiza estoque, soma gastos do cliente e total de vendas, e adiciona na fila de vendas.
- **6 - Ver fila de vendas**: lista a fila com as vendas registradas.
- **7 - Desfazer última operação**: desfaz o último cadastro/remoção/atualização/venda usando a pilha de operações.
- **8 - Exibir valor total do estoque**: soma de (quantidade × preço) de todos os produtos.
- **9 - Exibir valor total de vendas realizadas**: acumulado das vendas.
- **10 - Exibir clientes e valores totais gastos**: lista clientes com total gasto.
- **11 - Sair**: salva os dados e encerra.
- **12 - Salvar Dados**: persiste imediatamente em CSV.
- **13 - Remover cliente por ID**: remove cliente existente.
- **14 - Pesquisar produto por nome ou ID**: busca exata por ID ou parcial por nome.
- **15 - Atualizar quantidade de produto existente**: adiciona quantidade positiva ao estoque do produto.

### Entrada de dados
- Números inteiros (IDs e quantidades) aceitam apenas dígitos.
- Preços aceitam vírgula ou ponto como separador decimal (ex.: `12,50` ou `12.50`).

### Persistência e arquivos CSV
- Os arquivos são criados/atualizados automaticamente ao salvar ou sair do sistema.
- Codificação: UTF-8. Cabeçalhos são escritos nas três planilhas.
- Para resetar o estado, apague os CSVs antes de iniciar o programa.
- Na inicialização, o sistema carrega os dados existentes (clientes, produtos e vendas) e recalcula o total de vendas.

### Regras e validações importantes
- `ID` de cliente e de produto não podem se repetir.
- Cadastro de produto com nome já existente (normalizado) é bloqueado; use a opção 15 para ajustar quantidade.
- Não é permitido cadastrar produto com nome "girafa".
- Desfazer venda restaura estoque, total do cliente e total de vendas, além de remover a venda correspondente da fila.

### Exemplos rápidos
1. Cadastrar cliente (1) → ID `1`, Nome `Ana`.
2. Cadastrar produto (3) → ID `10`, Nome `Café`, Quantidade `50`, Preço `12,90`.
3. Realizar venda (5) → Cliente `1`, Produto `10`, Quantidade `2`.
4. Ver fila (6) → exibe a venda registrada.
5. Desfazer (7) → reverte a venda.

### Dicas
- Use a opção 12 (Salvar Dados) periodicamente durante testes.
- A saída (11) também salva automaticamente.

### Licença
Projeto acadêmico/educacional. Utilize livremente para estudo.

