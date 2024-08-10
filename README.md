# API_Pessoa

* Banco de dados usado nesse projeto é o PostgreSQL
* Para a contrução da api é usado a biblioteca FLASK

## variaveis de ambiente
no arquivo `config.py` está as configurações de acesso ao banco de dados. Será necessário criar um arquivo .env ou variaveis de ambiente no sistema com os seguintes dados:

* DB_HOST
* DB_NAME
* DB_USER
* DB_PASS 
* DB_PORT: o padrão do posgres é `5432`


# Rotas
### GET
* listar todos: `localhost:5000/pessoa`
* listar por ID: `localhost:5000/pessoa/<id>`

### POST
* inserir pessoa: `localhost:5000/pessoa/`

exemplo de body:
```
{
    "nome": "programador",
    "data": "01/05/2002",
    "salario": 1350,
    "obs": "",
    "nomemae": "Bernadethe",
    "nomepai": "Mário",
    "cpf": "123456"

}
```

### DELETE
* deletar pessoa: `localhost:5000/pessoa/delete/<id>`

### PUT
* atualizar pessoa: `localhost:5000/pessoa/update/<id>`

exemplo de body:
```
{
    "cpf": "654897",
    "data": "01/03/1997",
    "idPessoa": 3,
    "nome": "Joaquin",
    "nomemae": null,
    "nomepai": null,
    "obs": "prof",
    "salario": "800"

}
```




