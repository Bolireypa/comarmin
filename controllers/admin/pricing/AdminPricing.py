from flask_restx import Namespace, Resource, fields
from flask import request
from .api import api
from models import CmPricing
from datetime import datetime

from flask_jwt_extended import jwt_required

pricing = api.model('Pricing', {
    'ore': fields.String(required=True, description='Pricing name'),
    'short': fields.String(required=True, description='Pricing lastname'),
    'pricing': fields.List(fields.Float(description='Pricing element'))
})

@api.route('/')
class AdminPricing(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    # @api.doc(security="CmApiKey")
    # @jwt_required()
    def get(self):
        '''List all pricing table'''
        try:
            res = { "success": False }
            pricing = CmPricing.CmPricing.getAll()
            # print(pricing)
            data = []
            for p in pricing:
                data.append({
                    "id": p._id(),
                    "ore": p.ore,
                    "short": p.short,
                    "pricing": p.pricing,
                    # "cellphone": p.cellphone,
                    # "address": p.address,
                    # "membershipDate": p.membership_date.strftime("%Y-%m-%d"),
                    "state": p.state,
                    "created_at": p.created_at.strftime("%Y-%m-%d %H:%M"),
                    "updated_at": p.updated_at.strftime("%Y-%m-%d %H:%M"),
                })
            # print(data)
            res["pricing"] = data
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
    @api.expect(pricing, validate=True)
    @api.doc('AddPricing')
    # @api.doc(security="CmApiKey")
    # @jwt_required()
    def post(self):
        '''Add new pricing'''
        try:
            res = { 'success': False }
            req = request.get_json()
            print(req)
            pricing = CmPricing.CmPricing.createPricing(req)
            res["pricing"] = req
            res["msg"] = "Se agrego correctamente los datos"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al agregar los datos: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500

edit_pricing = api.model('Edit Pricing', {
    'pricing': fields.List(fields.Float(description='Pricing element'))
})

@api.route('/<pricing_id>')
class AdminOnePricing(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.expect(edit_pricing, validate=True)
    @api.doc('EditPricing')
    # @api.doc(params={"pricing_id": "unique pricing id"})
    @api.doc(security="CmApiKey", params={"pricing_id": "unique pricing id"})
    @jwt_required()
    def put(self, pricing_id):
        '''Edit new pricing'''
        try:
            res = { 'success': False }
            req = request.get_json()
            print(req)
            pricing = CmPricing.CmPricing.getById(pricing_id)
            pricing.pricing = {'ore': pricing.short, 'pricing': req['pricing']}
            pricing.updated_at = datetime.utcnow()
            pricing.update()
            res["pricing"] = req
            res["msg"] = "Se edito correctamente los datos"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al editar los datos: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500