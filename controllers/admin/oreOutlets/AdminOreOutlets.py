from flask_restx import Namespace, Resource, fields
from flask import request
from .api import api
from models import CmOreOutlet, CmPartner, CmCompany, CmUser, CmVehicle, CmDriver

from flask_jwt_extended import jwt_required

ore_outlet = api.model('OreOutlet', {
    'date': fields.String(required=True, description='Ore Outlet name'),
    'number': fields.Integer(required=True, description="Ore Outlet number"),    
    'section': fields.String(required=True, description='Ore Outlet section'),
    'quantity': fields.Integer(required=True, description="Ore Outlet quantity"),
    'weight': fields.Float(required=True, description="Ore Outlet weight"),
    'materialType': fields.String(required=True, description='Ore Outlet material type'),
    'minerals': fields.String(required=True, description='Ore Outlet minerals'),
    'partnerId': fields.String(required=True, description='Ore Outlet partner ID'),
    'companyId': fields.String(required=True, description='Ore Outlet company ID'),
    'driverId': fields.String(required=True, description='Ore Outlet driver ID'),
    'vehicleId': fields.String(required=True, description='Ore Outlet vehicle ID'),
    'userId': fields.String(required=True, description='Ore Outlet user ID'),
})

@api.route('/')
class AdminOreOutlets(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.doc(security="CmApiKey")
    @jwt_required()
    def get(self):
        '''List all ore outlets'''
        try:
            res = { "success": False }
            outlets = CmOreOutlet.CmOreOutlet.getAll()
            # print(users)
            data = []
            for o in outlets:
                outlet_partner = CmPartner.CmPartner.getById(o.cm_partner_id)
                op = {
                    "id": outlet_partner._id(),
                    "name": outlet_partner.name,
                    "lastname": outlet_partner.lastname,
                    "full_name": outlet_partner.name + ' ' + outlet_partner.lastname
                }
                olc = CmCompany.CmCompany.getById(o.cm_company_id)
                oc = {
                    "id": olc._id(),
                    "name": olc.name
                }
                old = CmDriver.CmDriver.getById(o.cm_driver_id)
                od = {
                    "id": old._id(),
                    "name": old.name,
                    "lastname": old.lastname,
                    "full_name": old.name + ' ' + old.lastname
                }
                olv = CmVehicle.CmVehicle.getById(o.cm_vehicle_id)
                ov = {
                    "id": olv._id(),
                    "license_plate": olv.license_plate
                }
                olu = CmUser.CmUser.getById(o.cm_user_id)
                ou = {
                    "id": olu._id(),
                    "name": olu.name,
                    "lastname": olu.lastname,
                    "full_name": olu.name + ' ' + olu.lastname
                }
                data.append({
                    "id": o._id(),
                    'date': o.date.strftime("%Y-%m-%d"),
                    'number': o.number,
                    'section': o.section,
                    'quantity': o.quantity,
                    'weight': o.weight,
                    'materialType': o.material_type,
                    'minerals': o.minerals,
                    'partner': op,
                    'company': oc,
                    'driver': od,
                    'vehicle': ov,
                    'user': ou,
                    # 'partnerId': o.cm_partner_id.__str__(),
                    # 'companyId': o.cm_company_id.__str__(),
                    # 'driverId': o.cm_driver_id.__str__(),
                    # 'vehicleId': o.cm_vehicle_id.__str__(),
                    # 'userId': o.cm_user_id.__str__(),
                    "state": o.state,
                    "created_at": o.created_at.strftime("%Y-%m-%d %H:%M"),
                    "updated_at": o.updated_at.strftime("%Y-%m-%d %H:%M"),
                })
            res["outlets"] = data
            res["success"] = True
            return res, 200
        except Exception as e:
          print(e)
          res["success"] = False
          res["msg"] = "Algio salió mal al obtener la lista de salidas de mineral"
          return res, 500

    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.expect(ore_outlet, validate=True)
    @api.doc('AddDriver')
    @api.doc(security="CmApiKey")
    @jwt_required()
    def post(self):
        '''Add new ore outlet'''
        try:
            res = { "success": False }
            req = request.get_json()
            print(req)
            driver = CmOreOutlet.CmOreOutlet.createOreOutlet(req)
            res["driver"] = req
            res["msg"] = "Se agrego correctamente la salida de mineral"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al agregar la salida de mineral: {0}. Por favor inténtelo nuevamente".format(e)
            return res, 500

    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    # @api.expect(ore_outlet, validate=True)
    # @api.doc('AddDriver')
    # @api.doc(security="CmApiKey")
    # @jwt_required()
    def delete(self):
        '''delete rows from table'''
        try:
            res = { "success": False }
            # req = request.get_json()
            # print(req)
            # driver = CmOreOutlet.CmOreOutlet.createOreOutlet(req)
            # res["driver"] = req
            CmOreOutlet.CmOreOutlet.deleteRows()
            res["msg"] = "Se elimino los registros"
            res["success"] = True
            return res, 200
        except Exception as e:
            print(e)
            res["success"] = False
            res["msg"] = "Algo salió mal al agregar la salida de mineral: {0}. Por favor inténtelo nuevamente".format(e)
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