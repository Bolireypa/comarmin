from flask_restx import Namespace, Resource, fields
from flask import request
from .api import api
from models import CmVehicle

from flask_jwt_extended import jwt_required

vehicle = api.model('Vehicle', {
    'vehicleType': fields.String(required=True, description='Vehicle type'),
    'model': fields.String(required=True, description='Vehicle model'),
    'licensePlate': fields.String(required=True, description='Vehicle license plate'),
    'color': fields.String(required=True, description='Vehicle color'),
})

vehicleUpdt = api.model('VehicleUpdt', {
    'id': fields.String(required=True, description='Vehicle id'),
    'vehicleType': fields.String(required=True, description='Vehicle type'),
    'model': fields.String(required=True, description='Vehicle model'),
    'licensePlate': fields.String(required=True, description='Vehicle license plate'),
    'color': fields.String(required=True, description='Vehicle color'),
})

@api.route('/')
class AdminVehicles(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.doc(security="CmApiKey")
    @jwt_required()
    # @api.marshal_list_with(cat)
    def get(self):
        '''List all vehicles'''
        try:
            res = { "success": False }
            vehicles = CmVehicle.CmVehicle.getAll()
            # print(users)
            data = []
            for v in vehicles:
                data.append({
                    "id": v._id(),
                    "vehicle_type": v.vehicle_type,
                    "model": v.model,
                    "license_plate": v.license_plate,
                    "color": v.color,
                    "state": v.state,
                    "created_at": v.created_at.strftime("%Y-%m-%d %H:%M"),
                    "updated_at": v.updated_at.strftime("%Y-%m-%d %H:%M"),
                })
            res["vehicles"] = data
            res["success"] = True
            return res, 200
        except Exception as e:
          print(e)
          res["success"] = False
          res["msg"] = "Algio salió mal al obtener la lista de vehiculos"
          return res, 500

    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.expect(vehicle, validate=True)
    @api.doc('AddVehicle')
    @api.doc(security="CmApiKey")
    @jwt_required()
    def post(self):
        '''Add new vehicle'''
        try:
            res = { 'success': False }
            req = request.get_json()
            print(req)
            new_vehicle = CmVehicle.CmVehicle.createVehicle(req)
            res["vehicle"] = req
            res["msg"] = "Se agrego correctamente el vehiculo"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al agregar el vehiculo: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500

    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.expect(vehicleUpdt, validate=True)
    @api.doc('EditVehicle')
    @api.doc(security="CmApiKey")
    @jwt_required()
    def put(self):
        '''Edit vehicle'''
        try:
            res = { 'success': False }
            req = request.get_json()
            print(req)
            vehicle = CmVehicle.CmVehicle.getById(req["id"])
            if not vehicle:
                return res, 404
            vehicle.vehicle_type = req["vehicleType"]
            vehicle.model = req["model"]
            vehicle.license_plate = req["licensePlate"]
            vehicle.color = req["color"]
            # user.phone = req["phone"]
            # user.email = req["email"]
            # user.birth_date = req["birthDate"]
            vehicle.update()
            res["vehicle"] = req
            res["msg"] = "Se modifico correctamente el vehiculo"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al modificar el vehiculo: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500

@api.route('/<id>')
class AdminVehicle(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    # @api.expect(partnerUpdt, validate=True)
    @api.doc('DisableVehicle')
    @api.doc(security="CmApiKey", params={"id": "id vehicle"})
    @jwt_required()
    def put(self, id):
        '''Disable vehicle'''
        try:
            res = { 'success': False }
            vehicle = CmVehicle.CmVehicle.getById(id)
            if not vehicle:
                return res, 404
            print(vehicle.state)
            if vehicle.state == True:
                vehicle.state = False
                vehicle.update()
                res["msg"] = "Se deshabilito correctamente el vehiculo"
            else:
                vehicle.state = True
                vehicle.update()
                res["msg"] = "Se habilito correctamente el vehiculo"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al modificar el estado de el vehiculo: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500