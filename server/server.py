import time
import requests
from flask import Flask, request
from flask_restful import Api, Resource, abort

app = Flask(__name__)
api = Api(app)

info = {"0": 0}

class game(Resource):

  def get(self,name, port):
    global info
    return info

  def post(self, name, port):
    global info

    try:
      return {"None": "None"}
    finally:
      info.update({name:{"ip": request.remote_addr, "port": port}}) ##[name] = [request.remote_addr, port]
      time.sleep(10)
      info.pop(name)


api.add_resource(game, "/game/<string:name>/<string:port>")

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug= True)
