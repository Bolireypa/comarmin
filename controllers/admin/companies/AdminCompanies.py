from flask_restx import Namespace, Resource, fields
from flask import request
from .api import api
from models import CmCompany

from flask_jwt_extended import jwt_required

company = api.model('Company', {
    'name': fields.String(required=True, description='Company name'),
    'city': fields.String(required=True, description='Company city'),
    'department': fields.String(required=True, description='Company department'),
    'phone': fields.Integer(min=1000000, required=True, description="Company phone contact. Example: 2258964"),
    'nit': fields.String(required=True, description='Company nit'),
})

companyUpdt = api.model('CompanyUpdt', {
    'id': fields.String(required=True, description='Company id'),
    'name': fields.String(required=True, description='Company name'),
    'city': fields.String(required=True, description='Company city'),
    'department': fields.String(required=True, description='Company department'),
    'phone': fields.Integer(min=1000000, required=True, description="Company phone contact. Example: 2258964"),
    'nit': fields.String(required=True, description='Company nit'),
})

@api.route('/')
class AdminCompanies(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.doc(security="CmApiKey")
    @jwt_required()
    def get(self):
        '''List all companies'''
        try:
            res = { "success": False }
            companies = CmCompany.CmCompany.getAll()
            # print(users)
            data = []
            for c in companies:
                data.append({
                    "id": c._id(),
                    "name": c.name,
                    "city": c.city,
                    "department": c.department,
                    "phone": c.phone,
                    "nit": c.nit,
                    "state": c.state,
                    "created_at": c.created_at.strftime("%Y-%m-%d %H:%M"),
                    "updated_at": c.updated_at.strftime("%Y-%m-%d %H:%M"),
                })
            # print(data)
            res["companies"] = data
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
    @api.expect(company, validate=True)
    @api.doc('AddUser')
    @api.doc(security="CmApiKey")
    @jwt_required()
    def post(self):
        '''Add new company'''
        try:
            res = { 'success': False }
            req = request.get_json()
            print(req)
            company = CmCompany.CmCompany.createCampany(req)
            res["user"] = req
            res["msg"] = "Se agrego correctamente la empresa"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al agregar a la empresa: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500

    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.expect(companyUpdt, validate=True)
    @api.doc('EditCompany')
    @api.doc(security="CmApiKey")
    @jwt_required()
    def put(self):
        '''Edit company'''
        try:
            res = { 'success': False }
            req = request.get_json()
            print(req)
            company = CmCompany.CmCompany.getById(req["id"])
            if not company:
                return res, 404
            company.name = req["name"]
            company.city = req["city"]
            company.department = req["department"]
            company.phone = req["phone"]
            company.nit = req["nit"]
            # company.membership_date = req["membershipDate"]
            company.update()
            res["company"] = req
            res["msg"] = "Se modifico correctamente la empresa"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al modificar la empresa: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500

@api.route('/<id>')
class AdminCompany(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    # @api.expect(partnerUpdt, validate=True)
    @api.doc('DisableCompany')
    @api.doc(security="CmApiKey", params={"id": "id company"})
    @jwt_required()
    def put(self, id):
        '''Disable company'''
        try:
            res = { 'success': False }
            company = CmCompany.CmCompany.getById(id)
            if not company:
                return res, 404
            print(company.state)
            if company.state == True:
                company.state = False
                company.update()
                res["msg"] = "Se deshabilito correctamente la empresa"
            else:
                company.state = True
                company.update()
                res["msg"] = "Se habilito correctamente la empresa"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al modificar el estado de la empresa: {0}. Por favor inténtelo nuevamente".format(e)
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