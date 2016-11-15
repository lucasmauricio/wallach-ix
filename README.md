# Balut

This is a project to develop **Collection API** for [Arrakis project](https://github.com/lucasmauricio/arrakis).
The User API is beeing built in Python, using the Flask framework.

## Environment's configuration

Some people recommended to work with Python on a virtual environment.
This protects the SO's Python and m

- [ ] TODO describe environment's creation

## Running the API

You can run the API by yourself in the terminal or you can use a Docker container to do that.
We recommend you to use Docker because you can do this in a isolated configuration with no impact in you SO.

### Running in Docker

- [ ] TODO fix this steps

comando para criar o container com base no Dockerfile:
docker build -t organizacional-srv .

comando para executar o container e iniciar o serviço automaticamente
docker run --name organ-serv -v /home/lucasm/workspace/works-experiment/microservices/organizacional:/app-src -p 7070:8000 srv-organizacional

para utilizar o serviço, é só acessar o endereço http://localhost:7070/enterprise

para debugar o funcionamento do serviço no container
docker run --name organ-serv --entrypoint=/bin/ash -it -v /home/lucasm/workspace/works-experiment/microservices/organizacional:/app-src -p 7070:8000 srv-organizacional

### Running in the console

- [ ] TODO fix this example

```shell
cd ../env-python/organizacional
source ../teste_env/bin/activate
```

## About the project's name

http://dune.wikia.com/wiki/Wallach_IX
