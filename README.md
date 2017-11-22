# Wallet test

A barebones Django app, which can easily be deployed to Heroku.

Url [Wallet test](https://stone-test-wallet.herokuapp.com/) 

## Running Locally

```
$ https://github.com/luiscaiaffa/stone.git
$ cd stone

$ pip install -r requirements

$ python manage.py migrate
$ python manage.py createsuperuser

$ python manage.py runserver
```

Your app should now be running on [localhost:8000](http://localhost:8000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
