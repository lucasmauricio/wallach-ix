# coding: utf-8

from flask import Flask, request, abort
from flask_json import FlaskJSON, json_response
import requests
import socket
import os
import logging
import sys

__all__ = ['make_json_app']

app = Flask("collection_app")
json = FlaskJSON(app)

enterprise_info = {"name": "My Fic Company", "shortname": "FicCO"}
collections = {1: {"name": "Marketing"}, 2: {"name": "Sales"}, 3: {"name": "Human Resources"}, 4: {"name": "Production"}, 5: {"name": "Financial"}}

#host_address = '0.0.0.0'
host_port = 0

@app.route("/enterprise")
def enterprise_api():
    if request.method == "GET":
        return json_response(enterprise_info)


@app.route("/collection/<int:collection_id>")
def collection_api(collection_id=None):
    try:
        if request.method == "GET":
            if collection_id:
                # TODO handle 410 error (Gone): http://flask.pocoo.org/docs/0.11/patterns/errorpages/
                # retorna uma noticia especifica
                return json_response(collection=collections[collection_id]), 200
            else:
                # retorna todas as notícias
                return json_response(collections=collections), 200

        elif request.method == "POST":
            if request.is_json:
                # se o request veio com o mimetype "json" usa os dados para inserir novas noticias
                collections.bulk_insert(request.json)
                return "Collection created successfully", 201

        elif request.method == "DELETE":
            # apaga uma noticia especifica
            del collections[collection_id]
            return "Collection deleted successfully", 204
    except Exception:
        abort(500)


#registrando API do serviço
def api_register(api_id, api_data):
    logging.debug("registrando o serviço '{}'".format(api_id))

    REGISTRADOR_API = 'http://localhost:8080/asset/'
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.put(REGISTRADOR_API+api_id, headers=headers, json=api_data)
        if r.status_code == requests.codes.created:
            logging.debug(" -registrado com sucesso: {}".format(r.status_code))
        else:
            logging.error(" -ocorreu erro no registro do serviço: {}".format(r.status_code))
            logging.debug(" ->resposta do registrador: " + r.text)
            sys.exit(1)
    except requests.exceptions.ConnectionError as ce:
        # http://dev.mobify.com/blog/http-requests-are-hard/
        logging.error("These aren't the domains we're looking for. '%s'." % REGISTRADOR_API)
        logging.debug(ce)
        sys.exit(1)
    except requests.exceptions.HTTPError as he:
        #TODO testar um bad request
        # Tell the user their URL was bad and try a different one
        logging.error("O serviço não pode ser iniciado porque ocorreu TooManyRedirects ao conectar no registrador em '%s'." % REGISTRADOR_API)
        logging.debug(he)
        sys.exit(1)
    except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout) as t:
        #TODO testar ou remover
        logging.error("It's not possible to register the service at '%s' because the server is too slow." % REGISTRADOR_API)
        logging.debug(t)
        sys.exit(1)
    except requests.exceptions.TooManyRedirects as tmr:
        #TODO testar ou remover
        logging.error("O serviço não pode ser iniciado porque ocorreu TooManyRedirects ao conectar no registrador em '%s'." % REGISTRADOR_API)
        logging.debug(tmr)
        sys.exit(1)
    except requests.exceptions.RequestException as re:
        #TODO testar ou remover
        # catastrophic error. bail.
        logging.error("O serviço não pode ser iniciado porque ocorreu erro '%s' ao conectar no registrador em '%s'." % (re.errno, REGISTRADOR_API))
        logging.debug(re)
        sys.exit(1)


@app.errorhandler(404)
def page_not_found_handler(e):
    return json_response(message="The resource requested was not found at this server.", status=404)


@app.errorhandler(500)
def internal_server_error_handler(e):
    return json_response(message="Something's gone wrong and the server could not deal with your request.", status=500)


def run_server(port):
    logging.debug("")
    logging.info("initializing the app and its 2 services")
#    print "the server's address is " + app.config['SERVER_NAME']
    logging.debug(app.config.get('SERVER_NAME'))
    logging.debug(app.config.get('PORT'))

    #registrando serviço enterprise_api
    enterprise_api_id = 'enterprise'
    #TODO automatizar a forma de recuperar o endereço do serviço
    payload = {'name':'Enterprise data', "address": "http://{}:{}/enterprise".format('localhost', port)}
    logging.debug(payload)
    api_register(enterprise_api_id, payload);

    #registrando serviço collections_api
    collections_api_id = 'collection'
    #TODO automatizar a forma de recuperar o endereço do serviço
    payload = {'name':'collections data', "address": "http://{}:{}/collection".format('localhost', port)}
    logging.debug(payload)
    api_register(collections_api_id, payload);

    app.run(host= '0.0.0.0', port=port, debug=False, use_reloader=False)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s [%(levelname)-5s]: %(message)s',
                        )
    logging.info("initializing the app")

    host_port = int(os.environ.get('PORT', 8000))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #TODO trocar ou não pelo endereço de rede da máquina??
    #sock.bind(('localhost', 0))
    #host_address, host_port = sock.getsockname()
    logging.info("==> a porta escolhida foi {}".format(host_port))
    #print "==> e meu IP {}".format(host_address)
    sock.close()

    run_server(host_port)
