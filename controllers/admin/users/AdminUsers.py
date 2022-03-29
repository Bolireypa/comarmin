from flask_restx import Namespace, Resource, fields
from flask import request
from .api import api
from models import CmUser

from flask_jwt_extended import jwt_required

user = api.model('User', {
    'name': fields.String(required=True, description='User name'),
    'lastname': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email. Example: user@gmail.com'),
    'password': fields.String(required=True, description='User password.'),
    'birthDate': fields.String(required=True, description='User birth date. Example: 1990-05-05'),
    'cellphone': fields.Integer(min=10000000, required=True, description="User cellphone number. Example: 77701012"),
})

userUpdt = api.model('UserUpdt', {
    'id': fields.String(required=True, description='User id'),
    'name': fields.String(required=True, description='User name'),
    'lastname': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email. Example: user@gmail.com'),
    'password': fields.String(required=False, description='User password.'),
    'birthDate': fields.String(required=False, description='User birth date. Example: 1990-05-05'),
    'cellphone': fields.Integer(min=10000000, required=True, description="User cellphone number. Example: 77701012"),
})

@api.route('/')
class AdminUsers(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    # @api.doc(security="CmApiKey")
    # @jwt_required()
    # @api.marshal_list_with(cat)
    def get(self):
        '''List all users'''
        try:
            res = { "success": False }
            users = CmUser.CmUser.getUsers()
            # print(users)
            data = []
            for u in users:
                data.append({
                    "id": u._id(),
                    "name": u.name,
                    "lastname": u.lastname,
                    "email": u.email,
                    "birthDate": u.birth_date.strftime("%Y-%m-%d"),
                    "phone": u.phone,
                    "cellphone": u.cellphone,
                    "state": u.state,
                    "created_at": u.created_at.strftime("%Y-%m-%d %H:%M"),
                    "updated_at": u.updated_at.strftime("%Y-%m-%d %H:%M"),
                })
            # print(data)
            res["users"] = data
            res["success"] = True
            return res, 200
        except Exception as e:
          print(e)
          res["success"] = False
          res["msg"] = "Algio salió mal al obtener la lista de usuarios"
          return res, 500

    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.expect(user, validate=True)
    @api.doc('AddUser')
    # @api.doc(security="CmApiKey")
    # @jwt_required()
    def post(self):
        '''Add new user'''
        try:
            res = { 'success': False }
            req = request.get_json()
            print(req)
            new_user = CmUser.CmUser.createUser(req)
            res["user"] = req
            res["msg"] = "Se agrego correctamente al usuario"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al un nuevo usuario: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500

    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.expect(userUpdt, validate=True)
    @api.doc('EditUser')
    @api.doc(security="CmApiKey")
    @jwt_required()
    def put(self):
        '''Edit user'''
        try:
            res = { 'success': False }
            req = request.get_json()
            print(req)
            user = CmUser.CmUser.getById(req["id"])
            if not user:
                return res, 404
            user.name = req["name"]
            user.lastname = req["lastname"]
            if req["password"] != '':
                user.password = req["password"]
            user.cellphone = req["cellphone"]
            user.phone = req["phone"]
            user.email = req["email"]
            user.birth_date = req["birthDate"]
            user.update()
            res["user"] = req
            res["msg"] = "Se modifico correctamente el usuario"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al modificar el usuario: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500

@api.route('/<id>')
class AdminUser(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    # @api.expect(partnerUpdt, validate=True)
    @api.doc('DisableUser')
    @api.doc(security="CmApiKey", params={"id": "id user"})
    @jwt_required()
    def put(self, id):
        '''Disable user'''
        try:
            res = { 'success': False }
            user = CmUser.CmUser.getById(id)
            if not user:
                return res, 404
            print(user.state)
            if user.state == True:
                user.state = False
                user.update()
                res["msg"] = "Se deshabilito correctamente el usuario"
            else:
                user.state = True
                user.update()
                res["msg"] = "Se habilito correctamente el usuario"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al modificar el estado de el usuario: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500