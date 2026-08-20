# Sistema de Apostas em Jogos da Copa do Mundo 2026

Sistema desenvolvido em Python para gerenciamento de apostas em partidas da Copa do Mundo de 2026.

O sistema permite que usuários realizem apostas utilizando pontos, acompanhem suas apostas, consultem partidas e participem de um ranking. Também possui um perfil de administrador, responsável pelo gerenciamento das partidas e pela consulta dos usuários e apostas cadastradas.

O projeto utiliza uma API externa para obter dados das partidas da Copa do Mundo e um banco de dados SQLite para persistência dos dados.

## Funcionalidades

### Usuário

- Criar uma conta;
- Realizar login;
- Alterar senha;
- Consultar resultados anteriores de uma seleção;
- Consultar partidas disponíveis para apostas;
- Consultar as odds de uma partida;
- Registrar uma aposta;
- Consultar suas apostas;
- Consultar o status de uma aposta;
- Aumentar o multiplicador de uma aposta;
- Consultar seu saldo de pontos;
- Consultar o ranking de usuários;
- Cancelar sua participação no sistema.

### Administrador

- Criar partidas utilizando dados obtidos pela API;
- Listar partidas cadastradas;
- Consultar detalhes de uma partida;
- Iniciar uma partida;
- Finalizar uma partida utilizando o resultado obtido pela API;
- Listar usuários cadastrados;
- Listar usuários ativos e inativos;
- Pesquisar usuários;
- Consultar as apostas realizadas em uma partida;
- Consultar o ranking.

## Tecnologias utilizadas

- Python
- SQLAlchemy
- Pydantic
- SQLite
- Requests
- python-dotenv
- football-data.org API

## Organização do projeto

O sistema foi desenvolvido seguindo uma arquitetura dividida em camadas:

- **Models:** representam as entidades armazenadas no banco de dados.
- **Schemas:** realizam a validação e transferência dos dados.
- **DAO:** responsável pelo acesso e persistência dos dados.
- **Services:** contém as regras de negócio do sistema.
- **Controllers:** fazem a comunicação entre as Views e os Services.
- **Views:** responsáveis pela interação com o usuário através do terminal.
- **Exceptions:** contém as exceções personalizadas do sistema.
- **API:** responsável pela comunicação com a API externa.

## Banco de dados

O projeto utiliza SQLite para persistência dos dados e SQLAlchemy como ORM.

As principais entidades armazenadas são:

- Usuários;
- Partidas;
- Apostas.

## API

O sistema utiliza a API do [football-data.org](https://www.football-data.org/) para obter os dados das partidas da Copa do Mundo de 2026.

Para utilizar a API é necessário possuir um token de autenticação.

Crie um arquivo `.env` na raiz do projeto:

```env
FOOTBALL_DATA_TOKEN=seu_token_aqui
```

O token não deve ser enviado para o repositório. Por esse motivo, o arquivo `.env` deve estar incluído no `.gitignore`.

## Instalação

Clone o repositório e acesse a pasta do projeto.

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual.

No Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração inicial do banco

Crie as tabelas do banco de dados:

```bash
python -m backend.database.create_tables
```

Depois, crie o administrador inicial:

```bash
python -m backend.database.seed_admin
```

## Executando o sistema

Com o ambiente virtual ativado, execute:

```bash
python -m main
```

## Administrador padrão

O administrador inicial é criado pelo `seed_admin.py`.

```text
Login: admin
Senha: Admin@123
```

O cadastro realizado através da aplicação cria apenas usuários comuns, impedindo que um usuário se cadastre diretamente como administrador.

## Sistema de apostas

Cada usuário inicia sua participação com 100 pontos.

As odds são calculadas de acordo com a quantidade de apostas realizadas em cada seleção. Para evitar divisão por zero e impedir que as odds iniciais sejam iguais a 1, o cálculo considera inicialmente um apostador virtual para cada seleção.

A odd é armazenada no momento em que a aposta é realizada e não é alterada posteriormente.

O usuário também pode aumentar o multiplicador de uma aposta enquanto a partida ainda estiver disponível, desde que possua pontos suficientes.

Após a finalização da partida, o sistema utiliza o placar para determinar as apostas ganhas e perdidas, atualizar os pontos dos usuários e atualizar o ranking.

## Autora

Janinne Silva Krauspenhar

Projeto desenvolvido para o curso de programação backend do Instituto Hardware BR.