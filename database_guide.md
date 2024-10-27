# MySQL installation & set up guide

## Install MySQL

1. Follow [this](https://dev.mysql.com/downloads/mysql/) link.
2. Choose your operating system.
3. Download installer file.
4. Run the installer file.
5. Follow installer instruction.
6. Enter a password for root user when installer prompt.

## Set up a database

1. ### **MacOS/Linux**

    Login to MySQL terminal as a root user.

    ```
    mysql -u root -p
    ```

    After execute command, enter root password that you've set before in installer.

    If mysql command not found run this command to add mysql to PATH.

    ```
    export PATH=/usr/local/mysql/bin:$PATH
    ```

    Then try to login into mysql with root user again.

    ### **Window**

    Run MySQL Command Line Client application

2. Inside MySQL terminal, create a database for storing a data.

    ```sql
    CREATE DATABASE pawnDB;
    ```

    pawnDB can be any valid database name.

## Configure environments.

-   In [sample.env](./sample.env)

    ```
    # MySQL configuration
    DATABASE_NAME=pawnDB
    DATABASE_USER=root
    DATABASE_PASSWORD=password
    DATABASE_HOST=localhost
    DATABASE_PORT=3306
    ```

    Replace pawnDB with name of database that you has created before.

    Replace root with username if you have created a new user.

    Replace password with root password, or user password if you have created a new user.
