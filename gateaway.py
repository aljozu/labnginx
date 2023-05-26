from flask import Flask
from flask import request, jsonify
from flask_mongoengine import MongoEngine
import urllib.request, json

app = Flask(__name__)

@app.route('/')
def report_by_country():
    country_arg = request.args.get('country')
    president = "http://127.0.0.1:6103/?country={}".format(country_arg)
    response = urllib.request.urlopen(president)
    dataPresident = response.read()
    list_presidentes = json.loads(dataPresident)

    pbi = "http://127.0.0.1:6102/?country={}".format(country_arg)
    response = urllib.request.urlopen(pbi)
    datapbi = response.read()
    list_pbi = json.loads(datapbi)

    holiday = "http://127.0.0.1:6101/?country={}".format(country_arg)
    response = urllib.request.urlopen(holiday)
    dataHoliday = response.read()
    list_holiday = json.loads(dataHoliday)

    report = Report(country_arg, list_pbi['pbi'], list_presidentes['president'], list_holiday)
    return jsonify(report.to_json())


class Report:
    def __init__(self, country, pbi, presidente, feriados) -> None:
        self.country = country
        self.pbi = pbi
        self.presidente = presidente
        self.feriados = feriados
    def to_json(self):
        return {"Country": self.country,
                "PBI": self.pbi,
                "Presidente": self.presidente,
                "Feriados" : self.feriados}



if __name__ == "__main__":
    app.run(debug=True, port=6105)

    