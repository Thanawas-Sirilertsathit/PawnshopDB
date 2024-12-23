# PawnshopDB : A data management web app for Pawnshops

A web application for managing pawnshop records, items and transactions powered by Django.

## Install via Docker

1. Build docker compose

    ```bash
    docker compose up --build
    ```

2. Open 127.0.0.1:8000 in your browser once docker compose completely built

3. Run this command in docker exec terminal and create a superuser to access admin package

    ```bash
    python manage.py createsuperuser
    ```

4. In case you want to have staffs in the web app, use admin to grant access in Profile.

5. Once you want to close the web app, run this command.

    ```bash
    docker compose down
    ```

## How to install

1. Create python virtual environment
    ```bash
    python -m venv .venv
    ```
2. Install python package

    For MacOS run these command before follow below instruction

    Install [brew](https://brew.sh) then

    ```bash
    brew install mysql-client pkg-config
    ```

    For window / Linux user run just this command

    ```bash
    pip install -r requirements.txt
    ```

3. Install nodejs follows [instruction](https://nodejs.org/en/download/package-manager)

4. Copy a file [sample.env](./sample.env) and create a new one called `.env`.

-   Fill in the information inside

5. Find path to npm and edit PATH_TO_NPM in `.env`.
    ```bash
    which npm
    ```

-   This will tell you about your path to npm file. Put it in `PATH_TO_NPM`.

6. Install daisy UI

-   Move to static_src directory

```bash
cd theme/
cd static_src/
```

-   Install daisy UI

```bash
npm i -D daisyui@latest
```

7. Install tailwind

    ```bash
    python manage.py tailwind install

    python manage.py tailwind build

    ```

8. Follow MySQL [installation & set up guide](./database_guide.md)

9. Migrate Django database

    ```bash
    python manage.py migrate
    ```

10. Collect static_src

    ```bash
    python manage.py collectstatic
    ```

11. Run server
    ```bash
    python manage.py runserver
    ```
