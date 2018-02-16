import pymongo
from datetime import datetime, date
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

client = pymongo.MongoClient('localhost', 27017)

app= Flask(_name_)
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
            return {"error":"This information is already in the system."}

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
            worktime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            member.update({"user.employee_number":username}, {"$push":{"worktime":{"datetime":worktime}}})
            return {"firstname":firstname, "lastname":lastname, "datetime":worktime}
        else:
            return {}

class WorkTime(Resource):
    def get(self):
        args = parser.parse_args()
        id = args['id']
        data = member.find_one({"user.employee_number":id})
        if data:
            firstname = data['user']['firstname']
            lastname = data['user']['lastname']
            worktime = data['worktime']
            return {"firstname":firstname,"lastname":lastname,"worktime":worktime}
        else:
            return {}

api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(WorkTime,'/api/worktime')

if _name_ == '_main_':
        app.run(host='0.0.0.0', port=5500)