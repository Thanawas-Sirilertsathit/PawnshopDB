# PawnshopDB : A data management web app for Pawnshops

A web application for managing pawnshop records, items and transactions powered by Django.

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

12. For make sure run tailwind build again
    ```bash
    python manage.py tailwind build
    ```

## Tailwind Modification (For devs)

1. Move to static_src directory (You can try step 4 first, if it does not work then move back to step 1 and do it respectively.)

```bash
cd theme/
cd static_src/
```

2. Install dependencies

```bash
npm install
```

3. Open new terminal which is in main directory then run this command

```bash
python manage.py collectstatic
```

4. Build tailwind

```bash
python manage.py tailwind build
```

## Migrate (For devs)

-   If you update model. After run this please also do the following command below.

```bash
python manage.py makemigrations
```

-   If your friend update model.

```bash
python manage.py migrate
```
