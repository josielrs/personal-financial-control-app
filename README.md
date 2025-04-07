# Bem Vindo ao Controle Financeiro Pessoal!

Este projeto é um backend de uma aplicação cujo propósito é auxiliar o usuário no controle de seus gastos mensais, registrando receitas, despesas e reservas num só lugar possibilitando ao usuário uma visão mais ampla de como sua vida financeira acontece, de onde vem as receitas, quanto elas são, e pra onde elas estão indo. Desta forma o usuário poderá tomar decisões mais estratégicas alinhadas com seus objetivos pessoais.



## ARQUIVOS

Segue abaixo uma descrição da estrutura do projeto

### database

Arquivos referente à base de dados da aplicação, aqui você encontra o arquivo da base de dados, o DER e o script de montagem da base.

### model

Classes que representam os modelos de dados manipulados pela aplicação. Cada classe representa uma tabela do banco de dados e se torna um objeto da aplicação.

### schemas

Classes que representam os dados de entrada e saida da API do sistema.

### services

Classes que implementam todas as operações que serão realizadas em cima dos objetos da aplicação, elas implementam as regras de negócio

### repository

Classes que implementam as operações de manipulação de dados no banco de dados

### api_json.json

Arquivo JSON da API para importar no POSTMAN.




## COMO EXECUTAR


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.




## DOCUMENTAÇÕES

Segue abaixo a documentação deste projeto

## DER

Segue abaixo o diagrama entidade e relacionamento do projeto

![Diagrama de Entidade e Relacionamento](./database/DER.png)

### FINANCIAL_CONTROL

Nessa tabela terá os meses controlados pelo usuário, em próximas versões ela terá features adicionais onde o usuário poderá abrir, fechar, simular sua finanças dentro de cada mês e ano desejados, de forma a manter o controle mensal das finanças do usuário mês a mês

### FINANCIAL_CONTROL_ENTRY

Nesta tabela o usuário associará as movimentações financeiras ao controle mensal, podendo dar à movimentação caracteristicas específicas dentro do respectivo mes e ano de controle

### FINANCIAL_ENTRY

Nesta tabela conterá as movimentações financeiras de RECEITA, RESERVA e DESPESAS

### CREDIT_CARD

Tabela com os cartões de crédito do usuário

### FINANCIAL_ENTRY_CATEGORY

Tabela com o cadastro de categorias para as movimentações

### ENTRY_TYPE

Tabela auxiliar com o tipo de movimentação RECEITA, RESERVA ou DESPESA

### VALUE_TYPE

Tabela auxiliar com o tipo de valor possivel para movimentação, FIXO ou VARIAVEL

### CREDIT_CARD_FLAG

Tabela auxiliar com as bandeiras de cartão disponiveis no sistema.



## API Documentation - SWAGGER

Abra o [http://localhost:5000/docs](http://localhost:5000/docs) no navegador para verificar a documentação das APIs.