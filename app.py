from gevent.pywsgi import WSGIServer
from flask import Flask
from flask import render_template


program = Flask(__name__)


@program.route("/api/v1/hello-world-4")
def hello():
    return "Hello world!"


server = WSGIServer(('127.0.0.1', 5000), program)
server.serve_forever()
