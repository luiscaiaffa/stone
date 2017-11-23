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

[card](https://stone-test-wallet.herokuapp.com/api/card) GET-POST / PUT-PATH-DELETE -> (/card/id/)

[wallet](https://stone-test-wallet.herokuapp.com/api/wallet/) GET-POST / PUT-PATH-DELETE -> (/wallet/id/)

[invoice](https://stone-test-wallet.herokuapp.com/api/invoice/) GET-POST 

[invoice](https://stone-test-wallet.herokuapp.com/api/invoice/) PATH -> (/invoice/id/pay) 




