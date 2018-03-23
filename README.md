# Django (Hacker-news clone)
This web application is intended to training purposes, in the context of a bootcamp, it implements a clone of the hacker news [website](https://news.ycombinator.com/)

## Backend: Django/ PostgreSQL

Tools:
- django 1.9
- python 3.6
- django-allauth 0.31.0
- psycopg2 2.7.4
- etc (check requirements.txt for more details)

How it works:

- Install python version 3.6, together with [pip](https://pip.pypa.io/en/stable/installing/) and [virtualenv](https://virtualenv.pypa.io/en/stable/installation/).
- Clone the repository from my [github](https://github.com/Mehdi6/bootcamp-hackernews), and place it in a new folder.
- Install a virtualenv:
    run the command line, place yourself inside the project's folder, then create your new virtualenv.
    Install the requirements by running the following command line: `pip install -r requirements.txt`

- Run the server
(1) First run the command : `python manage.py migrate`
(2) Then: `python manage.py runsslserver`
(3) The server is now running on https://localhost:8000/

## Frontend:

Tools:

- jQuery
- bootstrap 3.7.3
- CSS3
- HTML5

## What do I need to know to test the web application?

## Issue Reporting

If you have found a bug or feature request, please report them at the repository issues section.

## License

MIT

## Acknowledgements

Thanks to the quick starting [project](https://github.com/pyaf/allauthproject) by Rishabh Agrahari that demonstrate very well how to use django-allauth lib to authenticate with social accounts.