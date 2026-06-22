# Market System POO

Sistema de mercado executado no terminal, desenvolvido em Python para praticar Programação Orientada a Objetos, estruturas de dados e persistência em arquivos CSV.

## Objetivo

Simular operações básicas de cadastro, estoque e vendas. O sistema mantém clientes e produtos, registra vendas em uma fila, permite desfazer operações recentes por meio de uma pilha e salva os dados localmente.

## Contexto do desenvolvimento

O projeto foi desenvolvido como exercício de Programação Orientada a Objetos e estruturas de dados. A proposta foi aplicar classes, composição, fila, pilha e persistência simples em um fluxo que pudesse ser usado e verificado pelo terminal.

## Funcionalidades implementadas

- cadastro, listagem e remoção de clientes;
- cadastro e listagem de produtos;
- pesquisa de produtos por ID ou parte do nome;
- atualização da quantidade disponível;
- validação de IDs duplicados de clientes e produtos;
- validação de produtos duplicados pelo nome;
- realização de vendas com verificação de cliente, produto e estoque;
- fila de vendas realizadas;
- desfazer cadastro, remoção, venda ou atualização de estoque;
- cálculo do valor total do estoque;
- cálculo do valor total vendido;
- acompanhamento do valor total gasto por cliente;
- leitura e gravação de clientes, produtos e vendas em CSV;
- validação básica das entradas digitadas no menu.

## Conceitos praticados

- classes e objetos;
- encapsulamento de dados;
- composição entre classes;
- listas, conjuntos e dicionários;
- fila com `collections.deque`;
- pilha implementada sobre uma lista;
- leitura e escrita de arquivos CSV;
- tratamento de exceções;
- validação de entradas no terminal.

## Tecnologias

- Python 3;
- biblioteca padrão `csv`;
- biblioteca padrão `collections`;
- arquivos CSV para persistência local.

O projeto não possui dependências externas.

## Estrutura

```text
MarketSystemPOO/
├── main.py         # menu e leitura das entradas
├── sistema.py      # regras de negócio e persistência
├── clientes.py     # modelo de cliente
├── produto.py      # modelo de produto
├── fila.py         # estrutura de fila
├── Pilha.py        # estrutura de pilha
├── clientes.csv    # dados de exemplo dos clientes
├── produtos.csv    # dados de exemplo do estoque
└── vendas.csv      # dados de exemplo das vendas
```

## Instalação e execução

### Pré-requisito

- Python 3.10 ou superior.

Clone o repositório:

```bash
git clone https://github.com/ViniciusNoetzold/MarketSystemPOO.git
cd MarketSystemPOO
```

Execute no Windows:

```powershell
py main.py
```

Ou, quando o comando `python` estiver configurado:

```bash
python main.py
```

O sistema carrega automaticamente os arquivos CSV existentes no diretório atual. Ao escolher a opção de salvar ou sair pelo menu, esses arquivos são atualizados.

## Menu disponível

```text
1  - Cadastrar cliente
2  - Listar clientes
3  - Cadastrar produto
4  - Listar produtos
5  - Realizar venda
6  - Ver fila de vendas
7  - Desfazer última operação
8  - Exibir valor total do estoque
9  - Exibir valor total de vendas realizadas
10 - Exibir clientes e valores totais gastos
11 - Sair
12 - Salvar dados
13 - Remover cliente por ID
14 - Pesquisar produto por nome ou ID
15 - Atualizar quantidade de produto existente
```

## Persistência dos dados

Os dados são armazenados em três arquivos:

### `clientes.csv`

```csv
id,nome,total_gasto
110,Bernardo,7000.0
666,dinho,0.0
```

### `produtos.csv`

```csv
id,nome,quantidade,preco
700,Notebook,3,3500.0
333,banana,5,10.0
```

### `vendas.csv`

```csv
cliente,produto,quantidade,valor
dinho,banana,3,30.0
```

Esses exemplos correspondem aos arquivos atualmente incluídos no projeto. Eles podem ser substituídos pelos dados informados durante o uso.

## Como o desfazer funciona

Cada ação reversível é armazenada na classe `Pilha`. Quando o usuário escolhe a opção de desfazer, a operação mais recente é retirada da pilha e revertida:

- um produto ou cliente recém-cadastrado é removido;
- um cliente removido é restaurado;
- uma venda devolve a quantidade ao estoque e desconta o valor do cliente;
- uma atualização de quantidade é revertida.

As vendas também são mantidas em uma `Fila`, preservando a ordem em que foram registradas.

## Aprendizados e desafios técnicos

- separar a interface de terminal das regras de negócio;
- manter o estoque consistente durante vendas e operações de desfazer;
- evitar cadastros duplicados por ID ou nome normalizado;
- restaurar quantidade, total vendido e gasto do cliente ao desfazer uma venda;
- converter corretamente os dados carregados do CSV;
- validar entradas numéricas e textuais sem encerrar o programa.

O ponto mais delicado é a reversão de vendas, pois ela precisa atualizar várias estruturas ao mesmo tempo: estoque, total gasto do cliente, total geral vendido, fila de vendas e histórico de operações.

## Testes

O repositório ainda não possui testes automatizados. Para uma verificação manual:

1. cadastre um cliente e um produto;
2. realize uma venda;
3. confira a redução do estoque e o total gasto;
4. use a opção de desfazer;
5. confirme que os valores anteriores foram restaurados;
6. salve, feche e abra novamente para validar a persistência.

## Limitações atuais

- interface somente por terminal;
- persistência em CSV, sem banco de dados;
- não há testes automatizados;
- não há controle de acesso;
- os arquivos CSV são sobrescritos ao salvar;
- o sistema deve ser executado a partir da pasta do projeto para localizar os dados.

## Melhorias futuras

Possíveis evoluções, ainda não implementadas:

- criar testes automatizados para cadastros, vendas e operações de desfazer;
- usar caminhos baseados na localização do projeto, reduzindo a dependência do diretório atual;
- separar os dados de demonstração dos dados gerados durante a execução;
- melhorar as mensagens de validação e a organização do menu;
- avaliar uma camada de persistência com banco de dados em uma evolução posterior.

## Demonstração e capturas pendentes

Produza manualmente:

1. `01-menu-principal.png`: menu principal no terminal;
2. `02-cadastro-produtos.png`: cadastro e listagem de produtos;
3. `03-venda-realizada.png`: realização de uma venda;
4. `04-fila-vendas.png`: fila de vendas;
5. `05-desfazer-operacao.png`: estoque restaurado após desfazer;
6. `06-persistencia-csv.png`: arquivos CSV após o salvamento.

Salve as imagens em `docs/images/`. Use somente dados fictícios e oculte caminhos locais, nomes reais, e-mails, telefones e outras informações pessoais.
