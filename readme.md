testing out openfaas templates

```sh
faas-cli template pull https://github.com/launchql/openfaas-templates
```

list available templates

```sh
faas-cli new --list
```

create a new JS function for jobs

```sh
faas-cli new --lang node12-graphql my-new-js-function
faas-cli new --lang python2.7-graphql my-new-py-function
```