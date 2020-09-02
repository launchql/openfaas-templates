testing out openfaas templates

# get started

```sh
faas template pull https://github.com/launchql/openfaas-templates
```

list available templates

```sh
faas new --list
```

create a new JS function for jobs

```sh
faas new --lang node12-graphql my-js-function
faas new --lang python3-flask-graphql my-py-function
```

# caveats

* `package.json` is renamed to `handler.json` for node because of `babel-watch` during hotloading. So in effort to make the developer experience better, currently we use `handler.json`. Sorry if this bugs you!

# hotloading

for now, it only works with `docker-compose`, but here's an example compose file:

```yaml
version: "3.7"
services:
  postgres:
    container_name: bitg-postgres
    image: pyramation/postgres
    environment:
      - "POSTGRES_USER=postgres"
      - "POSTGRES_PASSWORD=password"
    ports:
      - "5432:5432"
    expose:
      - "5432"
    volumes:
      - ./packages:/sql-extensions
      - ./pgdata:/var/lib/postgresql/data

  example-python-fn:
    build:
      context: ./template/python3-flask-graphql
    ports:
      - 10102:10101
    environment:
      GRAPHQL_URL: http://launchql:7777/graphql
      PORT: 10101
      SERVER_NAME: 0.0.0.0
      FLASK_APP: /home/app/index.py
      FLASK_ENV: development
      fprocess: flask run --port 10101 --host 0.0.0.0

    volumes:
      - ./functions/example-python-fn:/home/app/function
    user: root
    command: sh -c "fwatchdog"
    links:
      - launchql

  example-node-fn:
    build:
      context: ./template/node12-graphql
      dockerfile: Dockerfile.development
    ports:
      - 10101:10101
    environment:
      GRAPHQL_URL: http://launchql:7777/graphql
      PORT: 10101
      fprocess: yarn run watch
    volumes:
      - ./functions/example-node-fn:/home/app/src/function
    user: root
    command: sh -c "fwatchdog"
    links:
      - launchql

  launchql:
    container_name: launchql
    image: pyramation/launchql:0.18.3-12.18.2-alpine3.11
    environment:
      PGUSER: postgres
      PGPASSWORD: password
      PGHOST: postgres
      PGPORT: 5432
      PGDATABASE: services-db
      SERVER_PORT: 7777
      SERVER_HOST: "0.0.0.0"
      SERVICE_SCHEMA: services_public
      SERVICE_TABLE: services
    command: launchql
    ports:
      - "7777:7777"
    expose:
      - "7777"
    links:
      - postgres

```