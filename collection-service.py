# coding: utf-8

from flask import Flask, request, jsonify
import requests
import socket
import os

__all__ = ['make_json_app']

app = Flask("collection_app")

enterprise_info = {"name": "My Fic Company", "shortname": "FicCO"}
departments = {1: {"name": "Marketing"}, 2: {"name": "Sales"}, 3: {"name": "Human Resources"}, 4: {"name": "Produção"}}

#host_address = '0.0.0.0'
host_port = 0

@app.route("/enterprise")
def enterprise_api(department_id=None):
    if request.method == "GET":
        return jsonify(enterprise_info)


@app.route("/department/<int:department_id>")
def department_api(department_id=None):
    if request.method == "GET":
        if department_id:
            # retorna uma noticia especifica
            return jsonify(department=departments[department_id])
        else:
            # retorna todas as notícias
            return jsonify(departments=departments)

    elif request.method == "POST":
        if request.is_json:
            # se o request veio com o mimetype "json" usa os dados para inserir novas noticias
            noticias.bulk_insert(request.json)
            return "Department created successfully", 201

    elif request.method == "DELETE":
        # apaga uma noticia especifica
        del departments[department_id]
        return "Department deleted successfully", 204


#registrando API do serviço
def api_register(api_id, api_data):
    print "registrando o serviço '{}'".format(api_id)

    REGISTRADOR_API = 'http://registrator-serv:8080/asset/'
    headers = {'Content-Type': 'application/json'}
    r = requests.put(REGISTRADOR_API+api_id, headers=headers, json=api_data)
    if r.status_code == 201:
        print " -registrado com sucesso: {}".format(r.status_code)
    else:
        print " -ocorreu erro no registro do serviço: {}".format(r.status_code)
        print " ->resposta do registrador: " + r.text


def run_server(port):
    print ""
    print ""
    print "initializing the app and its 2 services"
#    print "the server's address is " + app.config['SERVER_NAME']
    print app.config.get('SERVER_NAME')
    print app.config.get('PORT')

    #registrando serviço enterprise_api
    enterprise_api_id = 'enterprise'
    #TODO automatizar a forma de recuperar o endereço do serviço
    payload = {'name':'Enterprise data', "address": "http://{}:{}/enterprise".format('localhost', port)}
    print payload
    api_register(enterprise_api_id, payload);

    #registrando serviço departments_api
    departments_api_id = 'department'
    #TODO automatizar a forma de recuperar o endereço do serviço
    payload = {'name':'Departments data', "address": "http://{}:{}/department".format('localhost', port)}
    print payload
    api_register(departments_api_id, payload);

    app.run(host= '0.0.0.0', port=port, debug=True, use_reloader=False)


if __name__ == '__main__':
    #TODO fazer esse log funcionar
    app.logger.info("initializing the app")

    host_port = int(os.environ.get('PORT', 8000))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #TODO trocar ou não pelo endereço de rede da máquina??
    #sock.bind(('localhost', 0))
    #host_address, host_port = sock.getsockname()
    print "==> a porta escolhida foi {}".format(host_port)
    #print "==> e meu IP {}".format(host_address)
    sock.close()

    run_server(host_port)
