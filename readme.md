testing out openfaas templates

```sh
faas-cli template pull https://github.com/launchql/openfaas-templates
```

list available templates

```sh
faas-cli new --list
```

create a new function

```sh
faas-cli new --lang node12-graphql my-new-function
```