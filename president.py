from flask import Flask
from flask import request, jsonify
from flask_mongoengine import MongoEngine
import urllib.request, json

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'presidentdb',
    'host': '127.0.0.1',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

@app.route('/')
def report_by_country():
    country_arg = request.args.get('country')
    #print(country_arg)
    db_presidente = President.objects(country=country_arg).first()

    if not db_presidente:
        return jsonify({'error': 'data not found'})
    else:
        report = {'president' : db_presidente.presidente}
        return jsonify(report)


class President(db.Document):
    country = db.StringField()
    presidente = db.StringField()
    def to_json(self):
        return {"Country": self.country,
                "Presidente": self.presidente}
    
if __name__ == "__main__":
    app.run(debug=True, port=6103)