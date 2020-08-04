testing out openfaas templates

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