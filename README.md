# Wallet

Url [Wallet test](https://stone-test-wallet.herokuapp.com/) 

## Rodando local

```
$ git clone https://github.com/luiscaiaffa/stone.git
$ cd stone

$ pip install -r requirements

$ python manage.py migrate
$ python manage.py createsuperuser

$ python manage.py runserver

$ python manage.py test gettingstarted/apps/api/
```

Seu aplicativo agora deve estar rodando em [localhost:8000](http://localhost:8000/).

## Documentação

User default:
username:  stone
password: stone123

client_id: ZOWiyVlh4lBExIMnFL2HyjCfcUsTt7mVoXeRKpI7

client_secret: mcpgQ5PAYUmW03EvBl5ZICyqIIW61TXhAZr3MCYQNXtVRNnq26juAMUOBR2bUCD5xoYGcKePnFch53Z0uh69iIqb7vVNnp3htZ7A2TfHiumeBTXsT19mLECmyz5ZU4FA

End points

[token](https://stone-test-wallet.herokuapp.com/o/token/) POST

```
POST 
{
  "grant_type": "password",
  "username": "stone",
  "password": "stone123", 
  "client_id": "ZOWiyVlh4lBExIMnFL2HyjCfcUsTt7mVoXeRKpI7",
  "client_secret": "mcpgQ5PAYUmW03EvBl5ZICyqIIW61TXhAZr3MCYQNXtVRNnq26juAMUOBR2bUCD5xoYGcKePnFch53Z0uh69iIqb7vVNnp3htZ7A2TfHiumeBTXsT19mLECmyz5ZU4FA"
}
```

[card](https://stone-test-wallet.herokuapp.com/api/card) GET-POST / PUT-PATH-DELETE -> (/card/id/)

* Cria um ou mais cartões para o cliente, além de permite a edição e exclusão do mesmo.
Após um cartão ser adicionado na carteira(wallet) só poderá ser alterado caso o mesmo seja
previamente removido.

```
POST / PUT
{
  "number": "string",
  "due_date": 0,
  "credit_limit": 0,
  "exp_year": 0,
  "name": "string",
  "verification_value": "string",
  "exp_month": 0
}
```

[wallet](https://stone-test-wallet.herokuapp.com/api/wallet/) GET-POST / PUT-PATH-DELETE -> (/wallet/id/)

* Cria apenas uma wallet para o cliente adicionando os cartões selecionados, além de permite a edição e exclusão da mesma.

```
POST / PUT
{
  "cards": [
    9,
    10
  ],
  "limit": 0
}
```

[invoice](https://stone-test-wallet.herokuapp.com/api/invoice/) GET-POST 

* Cria uma fatura e escolhe automaticamente os cartões.

```
POST
{
  "price": 0,
  "pay": true,
  "due_date": "string",
  "description": "string"
}
```

[invoice](https://stone-test-wallet.herokuapp.com/api/invoice/) PATH -> (/invoice/id/pay) 

* Atualiza o status da fatura e libera os cartões.
```
POST
{
  "pay": false
}
```




