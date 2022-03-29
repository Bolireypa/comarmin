from flask_restx import Namespace, Resource, fields
from flask import request
from .api import api
from models import CmUser

from flask_jwt_extended import ( jwt_required, get_jwt_identity, create_access_token, create_refresh_token )

user = api.model('UserAuthData', {
    'email': fields.String(required=True, description='User email. Example: user@gmail.com'),
    'password': fields.String(required=True, description='User password.'),
})



@api.route('/')
class AdminAuth(Resource):
    # @api.response(500, "Internal error")
    # @api.response(200, "Success")
    # @api.response(404, "Not found")
    # @api.response(400, "Bad request")
    # @api.doc('ListUsers')
    # # @api.marshal_list_with(cat)
    # def get(self):
    #     '''List all users'''
    #     try:
    #         users = CmUser.CmUser.getUsers()
    #         print(users[0])
    #         data = []
    #         for u in users:
    #             data.append({
    #                 "name": u.name
    #             })
    #         print(data)
    #         users1 = [
    #             {'id': '1', 'name': 'Felix'},
    #         ]
    #         res = { "success": False }
    #         res["users"] = users1
    #         res["success"] = True
    #         return res, 200
    #     except Exception as e:
    #       print(e)
    #       res["success"] = False
    #       res["msg"] = "Algio salió mal al obtener la lista de usuarios"
    #       return res, 500

    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.expect(user, validate=True)
    @api.doc('AddUser')
    def post(self):
        '''Add new user'''
        try:
            res = { 'success': False }
            req = request.get_json()
            user = CmUser.CmUser.getUserByEmail(req["email"])
            print(user.password)

            if not user:
              res["msg"] = "Usuario no encontrado, email o contraseña no encontrado"
              return res, 404
            
            if user:
              if user.password != req["password"]:
                res["msg"] = "Contraseña incorrecta, intente nuevamente"
                return res, 400
              else:
                payload = { "userId": user.id, "userName": user.name, "userEmail": user.email }
                access_token = create_access_token( payload )
                refresh_token = create_refresh_token( payload )
                
                res["user"] = {
                  "id": user._id(),
                  "name": user.name,
                  "lastname": user.lastname,
                  "email": user.email,
                  "token": access_token,
                  "refreshToken": refresh_token,
                }
                res["msg"] = "Inicio de sesion correcto, bienvenido!!!"
                res["success"] = True
                return res, 200
            else:
              res["msg"] = "Usuario no existe"
              return res, 404
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al un nuevo usuario: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500

# @api.route('/<id>')
# @api.param('id', 'The cat identifier')
# @api.response(404, 'Cat not found')
# class Cat(Resource):
#     @api.doc('get_cat')
#     @api.marshal_with(cat)
#     def get(self, id):
#         '''Fetch a cat given its identifier'''
#         for cat in CATS:
#             if cat['id'] == id:
#                 return cat
#         api.abort(404)