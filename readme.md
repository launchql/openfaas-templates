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
    container_name: my-postgres
    image: pyramation/postgres
    environment:
      - "POSTGRES_USER=postgres"
      - "POSTGRES_PASSWORD=password"
    ports:
      - "5432:5432"
    expose:
      - "5432"
    volumes:
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

# developer notes

## how does it work for node12?

### install

look at the package.json, `prewatch` script. Essentially, only for development, when building the image via docker, the volume is NOT mounted. So there is an issue where the 2nd npm install, the handler.json's deps, was not actually getting run. So we mitigate this by calling `npm install` again, `prewatch` during running this app. 

This really only matters when you are using development mode, and using `babel-watch`. Otherwise things should work as normal.

### npmrc

Only in the production private version of node we add an entry into the `.npmrc` file temporarily during build step. In the development version, we actually store the npm token, and this is NOT suitable for production. DO NOT push the images built with the development version. You've been warned.

# development vs. production

## development

Use `docker-compose`:

```
docker-compose build --build-arg NPM_TOKEN=${NPM_TOKEN}
```

## production

Use `faas-cli`

```sh
faas-cli build -f $(FUNC_FILE) --build-arg NPM_TOKEN=${NPM_TOKEN}
```

## makefile

example `Makefile` for all cases

```
FUNC_FILE ?= './stack.dev.yml'
.PHONY: up down functions build templates check-env

functions: check-env
	which faas-cli || (echo "Please install 'faas-cli' package" && exit 1)
	faas-cli build -f $(FUNC_FILE) --build-arg NPM_TOKEN=${NPM_TOKEN}

templates:
	which faas-cli || (echo "Please install 'faas-cli' package" && exit 1)
	faas template pull https://github.com/launchql/openfaas-templates

build: check-env
	docker-compose build --build-arg NPM_TOKEN=${NPM_TOKEN}

up:
	docker-compose up

down:
	docker-compose down -v

check-env:
ifndef NPM_TOKEN
	$(error NPM_TOKEN is undefined)
endif
```

example `stack.dev.yaml`:

```yml
version: 1.0
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080
functions:
  send-email-verification:
    lang: node12-graphql-private
    handler: ./functions/send-email-verification
    image: send-email-verification:latest
    environment:
      GRAPHQL_URL: http://launchql-service.webinc.svc.cluster.local:7777/graphql
      INTERNAL_JOBS_API_URL: http://jobs-service.webinc.svc.cluster.local:23456/graphql
      MAILGUN_KEY_FILE: /run/secrets/mailgun_key
      MAILGUN_DEV_EMAIL: email@gmail.com
      MAILGUN_DOMAIN: mg.domain.com
      MAILGUN_FROM: support@domain.com
      MAILGUN_REPLY: noreply@domain.com
      scale_from_zero: true
      inactivity_duration: 1m
```