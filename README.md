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
