import pymongo
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

client = pymongo.MongoClient('localhost', 27017)

app= Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('firstname')
parser.add_argument('lastname')
parser.add_argument('employee_number')

db = client.db_work

member = db.member

class Register(Resource):
    def post(self):
        args = parser.parse_args()
        id = args['employee_number']
        firstname = args['firstname']
        lastname = args['lastname']
        password = args['password']
        data = member.find_one({"user.employee_number":id})
        if not data:
            member.insert({"user":{"employee_number":id, "firstname":firstname, "lastname":lastname, "password":password}, "worktime":[]})
            return {"firstname":firstname, "lastname":lastname, "employee_number":id, "password":password}
        else:
            return {"error"}

from datetime import datetime, date
class Login(Resource):
    def post(self):
	args = parser.parse_args()
	username = args['username']
	password = args['password']
        data = member.find_one({"user.employee_number":username, "user.password":password})
        print data
        if data:
            firstname = data['user']['firstname']
            lastname = data['user']['lastname']
            time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            member.update({"user.employee_number":username}, {"$push":{"time":{"datetime":time}}})
            return {"firstname":firstname, "lastname":lastname, "datetime":time}
        else:
            return {}

class WTime(Resource):
    def get(self):
        args = parser.parse_args()
        id = args['id']
        data = member.find_one({"user.employee_number":id})
        if data:
            firstname = data['user']['firstname']
            lastname = data['user']['lastname']
            Wtime = data['time']
            return {"firstname":firstname,"lastname":lastname,"time":Wtime}
        else:
            return {}

api.add_resource(Regis, '/api/regis')
api.add_resource(Login, '/api/login')
api.add_resource(WTime,'/api/time')

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5005)
