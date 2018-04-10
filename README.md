# Django (Hacker-news clone)
This web application is intended to training purposes, in the context of a bootcamp, it implements a clone of the hacker news [website](https://news.ycombinator.com/)

## Backend: Django/ PostgreSQL

Technologies:
- django
- python
- django-allauth
- psycopg2
- etc (check requirements/ for more details)

How it works:

- Install python version 3.6, together with [pip](https://pip.pypa.io/en/stable/installing/) and [virtualenv](https://virtualenv.pypa.io/en/stable/installation/).
- Clone the repository from my [github](https://github.com/Mehdi6/bootcamp-hackernews), and place it in a new folder.

Setting the server locally:

- Install a virtualenv:
    run the command line, place yourself inside the project's folder, then create your new virtualenv.
    Install the requirements by running the following command line: `pip3 install -r requirements/local.txt`

- Run the server
(1) Define the next environement variables:
    export DJANGO_SETTINGS_MODULE=project.settings.local
    export DJANGO_READ_DOT_ENV_FILE=False

(2) First run the command : `python3 manage.py migrate`

(3) Configure the social app using django admin, further details can be found following this [link](https://medium.com/@jinkwon711/django-allauth-facebook-login-b536444cbc6b)

(4) Then: `python3 manage.py runsslserver`

(5) The server is now running on https://localhost:8000/

Setting the server on production mode (Docker)

- Simply run the next command line `sudo docker-compose up --build -d`
- Read the log using the next command `sudo docker-compose logs`
- Now the server run on https://localhost:443/
- Configure the social app using django admin, further details can be found following this [link](https://medium.com/@jinkwon711/django-allauth-facebook-login-b536444cbc6b)

## Frontend:

Technologies:

- jQuery
- bootstrap
- CSS3
- HTML5

## Testing the web application

In order to test the app, there is a set of tests developped using the pytest-django lib.
Start by defining the next environment variables:
- export DJANGO_SETTINGS_MODULE=project.settings.local
- export DJANGO_READ_DOT_ENV_FILE=False

Then, simply run the next command `pytest`.

## Issue Reporting

If you have found a bug or feature request, please report them at the repository issues section.

## License

MIT

## Acknowledgements

Thanks to the quick starting [project](https://github.com/pyaf/allauthproject) by Rishabh Agrahari that demonstrate very well how to use django-allauth lib to authenticate with social accounts.