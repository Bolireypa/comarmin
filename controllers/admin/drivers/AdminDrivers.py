from flask_restx import Namespace, Resource, fields
from flask import request
from .api import api
from models import CmDriver

from flask_jwt_extended import jwt_required

driver = api.model('Driver', {
    'name': fields.String(required=True, description='Driver name'),
    'lastname': fields.String(required=True, description='Driver lastname'),
    'ci': fields.String(required=True, description='Driver CI'),
    'address': fields.String(required=True, description='Driver address'),
    'cellphone': fields.Integer(min=1000000, required=True, description="Driver cellphone"),
})

driverUpdt = api.model('DriverUpdt', {
    'id': fields.String(required=True, description='Driver id'),
    'name': fields.String(required=True, description='Driver name'),
    'lastname': fields.String(required=True, description='Driver lastname'),
    'ci': fields.String(required=True, description='Driver CI'),
    'address': fields.String(required=True, description='Driver address'),
    'cellphone': fields.Integer(min=1000000, required=True, description="Driver cellphone"),
})

@api.route('/')
class AdminDrivers(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.doc(security="CmApiKey")
    @jwt_required()
    def get(self):
        '''List all drivers'''
        try:
            res = { "success": False }
            drivers = CmDriver.CmDriver.getAll()
            # print(users)
            data = []
            for d in drivers:
                data.append({
                    "id": d._id(),
                    "name": d.name,
                    "lastname": d.lastname,
                    "ci": d.ci,
                    "cellphone": d.cellphone,
                    "address": d.address,
                    "state": d.state,
                    "created_at": d.created_at.strftime("%Y-%m-%d %H:%M"),
                    "updated_at": d.updated_at.strftime("%Y-%m-%d %H:%M"),
                })
            # print(data)
            res["drivers"] = data
            res["success"] = True
            return res, 200
        except Exception as e:
          print(e)
          res["success"] = False
          res["msg"] = "Algio salió mal al obtener la lista de conductores"
          return res, 500

    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.expect(driver, validate=True)
    @api.doc('AddDriver')
    @api.doc(security="CmApiKey")
    @jwt_required()
    def post(self):
        '''Add new driver'''
        try:
            res = { "success": False }
            req = request.get_json()
            print(req)
            driver = CmDriver.CmDriver.createDriver(req)
            res["driver"] = req
            res["msg"] = "Se agrego correctamente al conductor"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al agregar al conductor: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500

    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.expect(driverUpdt, validate=True)
    @api.doc('EditDriver')
    @api.doc(security="CmApiKey")
    @jwt_required()
    def put(self):
        '''Edit driver'''
        try:
            res = { 'success': False }
            req = request.get_json()
            print(req)
            driver = CmDriver.CmDriver.getById(req["id"])
            if not driver:
                return res, 404
            driver.name = req["name"]
            driver.lastname = req["lastname"]
            driver.ci = req["ci"]
            driver.cellphone = req["cellphone"]
            driver.address = req["address"]
            # partner.membership_date = req["membershipDate"]
            driver.update()
            res["driver"] = req
            res["msg"] = "Se modifico correctamente el conductor"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al modificar el conductor: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500

@api.route('/<id>')
class AdminDriver(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    # @api.expect(partnerUpdt, validate=True)
    @api.doc('DisableDriver')
    @api.doc(security="CmApiKey", params={"id": "id driver"})
    @jwt_required()
    def put(self, id):
        '''Disable driver'''
        try:
            res = { 'success': False }
            driver = CmDriver.CmDriver.getById(id)
            if not driver:
                return res, 404
            print(driver.state)
            if driver.state == True:
                driver.state = False
                driver.update()
                res["msg"] = "Se deshabilito correctamente el conductor"
            else:
                driver.state = True
                driver.update()
                res["msg"] = "Se habilito correctamente el conductor"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al modificar el estado de el conductor: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500