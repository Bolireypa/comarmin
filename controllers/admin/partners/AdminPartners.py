from flask_restx import Namespace, Resource, fields
from flask import request
from .api import api
from models import CmPartner

from flask_jwt_extended import jwt_required

partner = api.model('Partner', {
    'name': fields.String(required=True, description='Partner name'),
    'lastname': fields.String(required=True, description='Partner lastname'),
    'ci': fields.String(required=True, description='Partner CI'),
    'address': fields.String(required=True, description='Partner address'),
    'membershipDate': fields.String(required=True, description='Partner membership date'),
    'cellphone': fields.Integer(min=1000000, required=True, description="Partner cellphone"),
})

partnerUpdt = api.model('PartnerUpdt', {
    'id': fields.String(required=True, description='Partner Id'),
    'name': fields.String(required=True, description='Partner name'),
    'lastname': fields.String(required=True, description='Partner lastname'),
    'ci': fields.String(required=True, description='Partner CI'),
    'address': fields.String(required=True, description='Partner address'),
    'membershipDate': fields.String(required=True, description='Partner membership date'),
    'cellphone': fields.Integer(min=1000000, required=True, description="Partner cellphone"),
})

@api.route('/')
class AdminPartners(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.doc(security="CmApiKey")
    @jwt_required()
    def get(self):
        '''List all partners'''
        try:
            res = { "success": False }
            partners = CmPartner.CmPartner.getAll()
            # print(users)
            data = []
            for p in partners:
                data.append({
                    "id": p._id(),
                    "name": p.name,
                    "lastname": p.lastname,
                    "fullname": p.name + ' ' + p.lastname,
                    "ci": p.ci,
                    "cellphone": p.cellphone,
                    "address": p.address,
                    "membershipDate": p.membership_date.strftime("%Y-%m-%d"),
                    "state": p.state,
                    "created_at": p.created_at.strftime("%Y-%m-%d %H:%M"),
                    "updated_at": p.updated_at.strftime("%Y-%m-%d %H:%M"),
                })
            # print(data)
            res["partners"] = data
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
    @api.expect(partner, validate=True)
    @api.doc('AddPartner')
    @api.doc(security="CmApiKey")
    @jwt_required()
    def post(self):
        '''Add new partner'''
        try:
            res = { 'success': False }
            req = request.get_json()
            print(req)
            partner = CmPartner.CmPartner.createPartner(req)
            res["partner"] = req
            res["msg"] = "Se agrego correctamente al socio"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al agregar al socio: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500

    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.expect(partnerUpdt, validate=True)
    @api.doc('EditPartner')
    @api.doc(security="CmApiKey")
    @jwt_required()
    def put(self):
        '''Edit partner'''
        try:
            res = { 'success': False }
            req = request.get_json()
            print(req)
            partner = CmPartner.CmPartner.getById(req["id"])
            if not partner:
                return res, 404
            partner.name = req["name"]
            partner.lastname = req["lastname"]
            partner.ci = req["ci"]
            partner.cellphone = req["cellphone"]
            partner.address = req["address"]
            partner.membership_date = req["membershipDate"]
            partner.update()
            res["partner"] = req
            res["msg"] = "Se modifico correctamente al socio"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al modificar al socio: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500

@api.route('/<id>')
class AdminPartner(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    # @api.expect(partnerUpdt, validate=True)
    @api.doc('DisablePartner')
    @api.doc(security="CmApiKey", params={"id": "id partner"})
    @jwt_required()
    def put(self, id):
        '''Disable partner'''
        try:
            res = { 'success': False }
            # req = request.get_json()
            # print(req)
            partner = CmPartner.CmPartner.getById(id)
            if not partner:
                return res, 404
            print(partner.state)
            if partner.state == True:
                partner.state = False
                partner.update()
                res["msg"] = "Se deshabilito correctamente al socio"
            else:
                partner.state = True
                partner.update()
                res["msg"] = "Se habilito correctamente al socio"
            # partner.lastname = req["lastname"]
            # partner.ci = req["ci"]
            # partner.cellphone = req["cellphone"]
            # partner.address = req["address"]
            # partner.membership_date = req["membershipDate"]
            # res["partner"] = req
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al modificar el estado de socio: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500