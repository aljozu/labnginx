from flask import Flask
from flask import request, jsonify
from flask_mongoengine import MongoEngine
import urllib.request, json

app = Flask(__name__)

@app.route('/')
def get_holidays():
    country_arg = request.args.get('country')
    url = "https://date.nager.at/api/v2/publicholidays/2023/{}".format(country_arg)

    response = urllib.request.urlopen(url)
    data = response.read()
    list_feriados = json.loads(data)
    feriados = []
    # print(len(list_feriados))
    for valores in list_feriados:
        feriados.append(Holiday(valores["date"], valores["localName"]).__dict__)

    return feriados

class Holiday:
    def __init__(self, fecha, nombre):
        self.fecha = fecha
        self.nombre = nombre
    def to_json(self):
        return {"Fecha": self.fecha,
                "Nombre": self.nombre}


if __name__ == "__main__":
    app.run(debug=True, port=6101)