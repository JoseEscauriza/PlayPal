# Getting started

In order to get started contributing to this project, do the following:

1. Clone the repository
2. Once inside, create a Python 3.11 virtual enviroment (venv) and activate it
3. run make dev-install in your terminal
4. Create a Database called 'playpal' in PostgreSQL
5. Create a .env file inside the config directory (playpal/config/.env) and set up your enviroment variables like so:

    ```Python
    SECRET_KEY=key here
    DB_HOST=name here
    DB_NAME=playpal
    DB_USER=username here
    DB_PASSWORD=password here
    DB_PORT=port here (default 5432)
    ```

6. Create a super user to be able to access the Admin dashboard

    ```bash
    python manage.py createsuperuser --settings=config.settings.dev
    ```

7. To make sure everything is working properly, in your terminal: run the make command (alternatively make dev-start). If the server starts up with no issues, you're good to go.

8. Roll up them sleeves and get your hands dirty!