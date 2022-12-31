import os
import dotenv
import json
from flask import Flask,request,render_template
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import logging
from serializers import AlchemyEncoder
import socket
import fcntl
import struct

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'flask'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'flask')
)
db = SQLAlchemy(app)

class RawData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer)
    device = db.Column(db.String(120))
    name = db.Column(db.String(120))
    mimetype = db.Column(db.String(120))
    count = db.Column(db.Integer)
    gender_age = db.Column(db.String(120))
    timestamp = db.Column(db.String(120))

    def __repr__(self):
        return '<RawData %r>' % self.device


# create the DB on demand
@app.before_first_request
def create_tables():
    db.create_all()


class JustData(Resource):
    def get(self):
        ret = []
        res = RawData.query.all()
        for i in res:
            ret.append(
                {
                    'site_id': i.site_id,
                    'device': i.device,
                    'name': i.name,
                    'mimetype': i.mimetype,
                    'count':i.count,
                    'gender_age': i.gender_age,
                    'timestamp': i.timestamp,
                }
            )
        return ret, 200


api.add_resource(JustData, '/rawdata')

@app.route('/', methods = ['GET','POST'])
def hello():
    logging.info('Hello World')
    data = dict(os.environ.items())

    if request.method == 'POST':
        env_keys = list(request.form.keys())
        for i in env_keys:
            os.environ[i] = request.form[i]
            dotenv.set_key(dotenv_file, i, os.environ[i])

        result = dict(os.environ.items())
        return result

    
    return render_template('index.html',result=data,localip = os.getenv('MYV4IP'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
