from flask_restx import Namespace, Resource, fields, inputs
from flask import request
from .api import api
from models import CmPartner, CmCompany, CmOreOutlet, CmDriver, CmVehicle

from flask_jwt_extended import jwt_required

from datetime import datetime, timedelta

# partner = api.model('Partner', {
#     'name': fields.String(required=True, description='Partner name'),
#     'lastname': fields.String(required=True, description='Partner lastname'),
#     'ci': fields.String(required=True, description='Partner CI'),
#     'address': fields.String(required=True, description='Partner address'),
#     'membershipDate': fields.String(required=True, description='Partner membership date'),
#     'cellphone': fields.Integer(min=1000000, required=True, description="Partner cellphone"),
# })

parserCompp = api.parser()
parserCompp.add_argument("date1", type=inputs.datetime_from_iso8601, required=True, help="Max value is the current date. Example: 2020-06-10")
parserCompp.add_argument("date2", type=inputs.datetime_from_iso8601, required=True, help="Max value is the current date. Example: 2020-07-01")
parserCompp.add_argument("companyId", type=str, required=False, help="Company ID. Example: 101293-1230123,10239-1923,12312-21323")

@api.route('/')
class AdminReports(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.doc(security="CmApiKey")
    @api.expect(parserCompp, validate=True)
    @jwt_required()
    def get(self):
        '''Get ore outlet company report'''
        try:
            res = { "success": False }
            filters = parserCompp.parse_args()
            print(filters)
            company = CmCompany.CmCompany.getById(filters["companyId"])
            if not company:
              return res, 404
            data = {
              "id": company._id(),
              "name": company.name,
              "city": company.city,
              "phone": company.phone,
              "nit": company.nit,
              "outlets": []
            }
            min_date = ''
            max_date = ''
            if (filters["date1"] < filters["date2"]):
              print("date1 < date2")
              min_date = filters["date1"]
              max_date = filters["date2"]
            if (filters["date1"] > filters["date2"]):
              print("date1 > date2")
              max_date = filters["date1"]
              min_date = filters["date2"]
            if (filters["date1"] == filters["date2"]):
              print("date1 = date2")
              min_date = filters["date1"]
              max_date = filters["date2"]
            # print(min_date, max_date)
            outlet_company = CmOreOutlet.CmOreOutlet.oreOutletByCompany(filters["companyId"],min_date,max_date)
            print(outlet_company)
            for oc in outlet_company:
              outlet_partner = CmPartner.CmPartner.getById(oc.cm_partner_id)
              old = CmDriver.CmDriver.getById(oc.cm_driver_id)
              olv = CmVehicle.CmVehicle.getById(oc.cm_vehicle_id)
              
              data["outlets"].append({
                "id": oc._id(),
                'date': oc.date.strftime("%Y-%m-%d"),
                'number': oc.number,
                'section': oc.section,
                'quantity': oc.quantity,
                'weight': oc.weight,
                'materialType': oc.material_type,
                'minerals': oc.minerals,
                'partner': outlet_partner.name + ' ' + outlet_partner.lastname,
                'driver': old.name + ' ' + old.lastname,
                'vehicle': olv.license_plate
              })
            # print(data)
            res["report"] = data
            res["success"] = True
            return res, 200
        except Exception as e:
          print(e)
          res["success"] = False
          res["msg"] = "Algio salió mal al obtener el reporte"
          return res, 500

partnerParser = api.parser()
partnerParser.add_argument("date1", type=inputs.datetime_from_iso8601, required=True, help="Max value is the current date. Example: 2020-06-10")
partnerParser.add_argument("date2", type=inputs.datetime_from_iso8601, required=True, help="Max value is the current date. Example: 2020-07-01")
partnerParser.add_argument("partnerId", type=str, required=False, help="Partner ID. Example: 101293-1230123,10239-1923,12312-21323")

@api.route('/outlet/partner/')
class AdminOutletPartnerReports(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.doc(security="CmApiKey")
    @api.expect(partnerParser, validate=True)
    @jwt_required()
    def get(self):
        '''Get ore outlet partner report'''
        try:
            res = { "success": False }
            filters = partnerParser.parse_args()
            partner = CmPartner.CmPartner.getById(filters["partnerId"])
            data = {
              "id": partner._id(),
              "name": partner.name,
              "cellphone": partner.cellphone,
              "outlets": []
            }
            min_date = ''
            max_date = ''
            if (filters["date1"] < filters["date2"]):
              print("date1 < date2")
              min_date = filters["date1"]
              max_date = filters["date2"]
            if (filters["date1"] > filters["date2"]):
              print("date1 > date2")
              max_date = filters["date1"]
              min_date = filters["date2"]
            if (filters["date1"] == filters["date2"]):
              print("date1 = date2")
              min_date = filters["date1"]
              max_date = filters["date2"]
            # print(min_date, max_date)
            outlet_partners = CmOreOutlet.CmOreOutlet.oreOutletByPartner(filters["partnerId"],min_date,max_date)
            print(outlet_partners)
            for oc in outlet_partners:
              # olp = CmPartner.CmPartner.getById(oc.cm_partner_id)
              old = CmDriver.CmDriver.getById(oc.cm_driver_id)
              olv = CmVehicle.CmVehicle.getById(oc.cm_vehicle_id)
              olc = CmCompany.CmCompany.getById(oc.cm_company_id)
              
              data["outlets"].append({
                "id": oc._id(),
                'date': oc.date.strftime("%Y-%m-%d"),
                'number': oc.number,
                'section': oc.section,
                'quantity': oc.quantity,
                'weight': oc.weight,
                'materialType': oc.material_type,
                'minerals': oc.minerals,
                # 'partner': olp.name + ' ' + olp.lastname,
                'driver': old.name + ' ' + old.lastname,
                'vehicle': olv.license_plate,
                'company': olc.name
              })
            # print(data)
            res["report"] = data
            res["success"] = True
            return res, 200
        except Exception as e:
          print(e)
          res["success"] = False
          res["msg"] = "Algio salió mal al obtener el reporte"
          return res, 500

partnerParserList = api.parser()
# partnerParser.add_argument("date1", type=inputs.datetime_from_iso8601, required=True, help="Max value is the current date. Example: 2020-06-10")
# partnerParser.add_argument("date2", type=inputs.datetime_from_iso8601, required=True, help="Max value is the current date. Example: 2020-07-01")
partnerParserList.add_argument("partnerId", type=str, required=False, help="Partner ID. Example: 101293-1230123,10239-1923,12312-21323")

@api.route('/outlet/partner/list/')
class AdminOutletPartnerListReports(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.doc(security="CmApiKey")
    @api.expect(partnerParserList, validate=True)
    @jwt_required()
    def get(self):
        '''Get ore outlet partner report list'''
        try:
            res = { "success": False }
            filters = partnerParserList.parse_args()
            partner = CmPartner.CmPartner.getById(filters["partnerId"])
            data = {
              "id": partner._id(),
              "name": partner.name,
              "cellphone": partner.cellphone,
              "outlets": []
            }
            # min_date = ''
            # max_date = ''
            # if (filters["date1"] < filters["date2"]):
            #   print("date1 < date2")
            #   min_date = filters["date1"]
            #   max_date = filters["date2"]
            # if (filters["date1"] > filters["date2"]):
            #   print("date1 > date2")
            #   max_date = filters["date1"]
            #   min_date = filters["date2"]
            # if (filters["date1"] == filters["date2"]):
            #   print("date1 = date2")
            #   min_date = filters["date1"]
            #   max_date = filters["date2"]
            # print(min_date, max_date)
            outlet_partners = CmOreOutlet.CmOreOutlet.oreOutletByPartnerList(filters["partnerId"])
            print(outlet_partners)
            for oc in outlet_partners:
              # olp = CmPartner.CmPartner.getById(oc.cm_partner_id)
              old = CmDriver.CmDriver.getById(oc.cm_driver_id)
              olv = CmVehicle.CmVehicle.getById(oc.cm_vehicle_id)
              olc = CmCompany.CmCompany.getById(oc.cm_company_id)
              
              data["outlets"].append({
                "id": oc._id(),
                'date': oc.date.strftime("%Y-%m-%d"),
                'number': oc.number,
                'section': oc.section,
                'quantity': oc.quantity,
                'weight': oc.weight,
                'materialType': oc.material_type,
                'minerals': oc.minerals,
                # 'partner': olp.name + ' ' + olp.lastname,
                'driver': old.name + ' ' + old.lastname,
                'vehicle': olv.license_plate,
                'company': olc.name
              })
            # print(data)
            res["report"] = data
            res["success"] = True
            return res, 200
        except Exception as e:
          print(e)
          res["success"] = False
          res["msg"] = "Algio salió mal al obtener el reporte"
          return res, 500

partnerParserOnly = api.parser()
partnerParserOnly.add_argument("date1", type=inputs.datetime_from_iso8601, required=True, help="Max value is the current date. Example: 2020-06-10")
partnerParserOnly.add_argument("date2", type=inputs.datetime_from_iso8601, required=True, help="Max value is the current date. Example: 2020-07-01")
# partnerParserOnly.add_argument("partnerId", type=str, required=False, help="Partner ID. Example: 101293-1230123,10239-1923,12312-21323")

@api.route('/outlet/partner/<partner_id>')
class AdminOutletPartnerOnlyReports(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    # security="CmApiKey", 
    @api.doc(params={"partner_id": "partner id"})
    @api.expect(partnerParserOnly, validate=True)
    # @jwt_required()
    def get(self, partner_id):
        '''Get ore outlet individual partner report'''
        try:
            res = { "success": False }
            filters = partnerParserOnly.parse_args()
            partner = CmPartner.CmPartner.getById(partner_id)
            data = {
              "id": partner._id(),
              "name": partner.name,
              "cellphone": partner.cellphone,
              "outlets": [],
              "labels": []
            }
            min_date = ''
            max_date = ''
            if (filters["date1"] < filters["date2"]):
              print("date1 < date2")
              min_date = filters["date1"].strftime("%Y-%m-%d")
              max_date = filters["date2"].strftime("%Y-%m-%d")
            if (filters["date1"] > filters["date2"]):
              print("date1 > date2")
              max_date = filters["date1"].strftime("%Y-%m-%d")
              min_date = filters["date2"].strftime("%Y-%m-%d")
            if (filters["date1"] == filters["date2"]):
              print("date1 = date2")
              min_date = filters["date1"].strftime("%Y-%m-%d")
              max_date = filters["date2"].strftime("%Y-%m-%d")
            print(min_date, max_date)
            # outlet_partners = CmOreOutlet.CmOreOutlet.oreOutletByPartnerList(partnerId)
            # print(outlet_partners)
            # for oc in outlet_partners:
            #   # olp = CmPartner.CmPartner.getById(oc.cm_partner_id)
            #   old = CmDriver.CmDriver.getById(oc.cm_driver_id)
            #   olv = CmVehicle.CmVehicle.getById(oc.cm_vehicle_id)
            #   olc = CmCompany.CmCompany.getById(oc.cm_company_id)
              
            #   data["outlets"].append({
            #     "id": oc._id(),
            #     'date': oc.date.strftime("%Y-%m-%d"),
            #     'number': oc.number,
            #     'section': oc.section,
            #     'quantity': oc.quantity,
            #     'weight': oc.weight,
            #     'materialType': oc.material_type,
            #     'minerals': oc.minerals,
            #     # 'partner': olp.name + ' ' + olp.lastname,
            #     'driver': old.name + ' ' + old.lastname,
            #     'vehicle': olv.license_plate,
            #     'company': olc.name
            #   })

            def fillDates(start, end):
              delta = end - start
              days = [start + timedelta(days = i) for i in range(delta.days + 1)]
              return days
            total_days = fillDates(filters["date1"], filters["date2"])
            str_total_days = []
            # print(total_days)
            datasets = []
            for t in total_days:
              str_total_days.append(t.strftime("%Y-%m-%d"))

            query_outlets = CmOreOutlet.CmOreOutlet.outletByPartnerAndDate(partner_id,min_date,max_date)
            print(query_outlets)
            result_array = [[],[]]
            for q in query_outlets:
              result_array[0].append(q[0].strftime("%Y-%m-%d"))
              result_array[1].append(q[1])
            d = []
            for t in total_days:
              # str_total_days.append(t.strftime("%Y-%m-%d"))
              if t.strftime("%Y-%m-%d") in result_array[0]:
                d.append(result_array[1][result_array[0].index(t.strftime("%Y-%m-%d"))])
                # print(result_array[0].index(t.strftime("%Y-%m-%d")))
              else:
                d.append(0)
            # # print(d)
            # datasets.append({
              # "label": partner.name,
              # "data": d,
              # "fill": False,
              # "borderColor": 'rgb(75, 192, 192)',
              # "tension": 0.5
            # })
            data["outlets"] = d
            data["labels"] = str_total_days
            # print(datasets)
            # res["labels"] = labels
            res["report"] = data
            res["success"] = True
            return res, 200
        except Exception as e:
          print(e)
          res["success"] = False
          res["msg"] = "Algio salió mal al obtener el reporte"
          return res, 500


dashParser = api.parser()
dashParser.add_argument("date1", type=inputs.datetime_from_iso8601, required=True, help="Max value is the current date. Example: 2020-06-10")
dashParser.add_argument("date2", type=inputs.datetime_from_iso8601, required=True, help="Max value is the current date. Example: 2020-07-01")
dashParser.add_argument("partnerId", type=str, required=False, help="Partner ID. Example: 101293-1230123,10239-1923,12312-21323")
dashParser.add_argument("getBy", type=str, required=False, help="Select how to get the chart by, exmaple: company, partner, vehicle, outlet")
# dashParser.add_argument("companyIds", type=str, action="split", required=False, help="Serie of comapny ID's to get stats from them. Example: 101293-1230123,10239-1923,12312-21323")

@api.route('/outlet/chart/')
class AdminOutletChartReports(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    # @api.doc(security="CmApiKey")
    @api.expect(dashParser, validate=True)
    # @jwt_required()
    def get(self):
        '''Get ore outlet report'''
        try:
            res = { "success": False }
            filters = dashParser.parse_args()
            # outlet = CmOreOutlet.CmOreOutlet.outletByCompanyAndDate(filters["partnerId"])
            # data = {
            #   "id": partner._id(),
            #   "name": partner.name,
            #   "cellphone": partner.cellphone,
            #   "outlets": []
            # }
            min_date = ''
            max_date = ''
            if (filters["date1"] < filters["date2"]):
              print("date1 < date2")
              min_date = filters["date1"]
              max_date = filters["date2"]
            if (filters["date1"] > filters["date2"]):
              print("date1 > date2")
              max_date = filters["date1"]
              min_date = filters["date2"]
            if (filters["date1"] == filters["date2"]):
              print("date1 = date2")
              min_date = filters["date1"]
              max_date = filters["date2"]
            # print(min_date, max_date)
            # get all dates between 2 dates
            def fillDates(start, end):
              delta = end - start
              days = [start + timedelta(days = i) for i in range(delta.days + 1)]
              return days
            total_days = fillDates(filters["date1"], filters["date2"])
            str_total_days = []
            # print(total_days)
            datasets = []
            title = ''
            for t in total_days:
              str_total_days.append(t.strftime("%Y-%m-%d"))
            
            if filters["getBy"] == "company":
              allComp = CmCompany.CmCompany.getAll()
              for c in allComp:

                query_outlets = CmOreOutlet.CmOreOutlet.outletByCompanyAndDate(c._id(),min_date,max_date)
                result_array = [[],[]]
                for q in query_outlets:
                  result_array[0].append(q[0].strftime("%Y-%m-%d"))
                  result_array[1].append(q[1])
                d = []
                for t in total_days:
                  # str_total_days.append(t.strftime("%Y-%m-%d"))
                  if t.strftime("%Y-%m-%d") in result_array[0]:
                    d.append(result_array[1][result_array[0].index(t.strftime("%Y-%m-%d"))])
                    # print(result_array[0].index(t.strftime("%Y-%m-%d")))
                  else:
                    d.append(0)
                # print(d)
                datasets.append({
                  "label": c.name,
                  "data": d,
                  "fill": False,
                  "borderColor": 'rgb(75, 192, 192)',
                  "tension": 0.5
                })
                title = 'Salidas de mineral - Empresa'
            
            if filters["getBy"] == "partner":
              allPart = CmPartner.CmPartner.getAll()
              for c in allPart:

                query_outlets = CmOreOutlet.CmOreOutlet.outletByPartnerAndDate(c._id(),min_date,max_date)
                result_array = [[],[]]
                for q in query_outlets:
                  result_array[0].append(q[0].strftime("%Y-%m-%d"))
                  result_array[1].append(q[1])
                d = []
                for t in total_days:
                  # str_total_days.append(t.strftime("%Y-%m-%d"))
                  if t.strftime("%Y-%m-%d") in result_array[0]:
                    d.append(result_array[1][result_array[0].index(t.strftime("%Y-%m-%d"))])
                    # print(result_array[0].index(t.strftime("%Y-%m-%d")))
                  else:
                    d.append(0)
                # print(d)
                datasets.append({
                  "label": c.name,
                  "data": d,
                  "fill": False,
                  "borderColor": 'rgb(75, 192, 192)',
                  "tension": 0.5
                })
                title = 'Salidas de mineral - Socio'

            if filters["getBy"] == "outlet":
              queryResult = CmOreOutlet.CmOreOutlet.outletByDate(min_date, max_date)
              # print(queryResult)
              result_array = [[],[]]
              for q in queryResult:
                # print(q[0])
                result_array[0].append(q[0].strftime("%Y-%m-%d"))
                result_array[1].append(q[1])
              # print(result_array)
                # if q[0].strftime("%Y-%m-%d") in str_total_days:
                  # print('exist')
                  # data.append(q[1])
              d = []
              ## ##
              for t in total_days:
                # str_total_days.append(t.strftime("%Y-%m-%d"))
                if t.strftime("%Y-%m-%d") in result_array[0]:
                  d.append(result_array[1][result_array[0].index(t.strftime("%Y-%m-%d"))])
                  # print(result_array[0].index(t.strftime("%Y-%m-%d")))
                else:
                  d.append(0)
              datasets.append({
                "label": "Salidas de mineral",
                "data": d,
                "fill": False,
                "borderColor": 'rgb(75, 192, 192)',
                "tension": 0.5
              })
              title = 'Salidas de mineral'
              # query_outlets = CmOreOutlet.CmOreOutlet.outletByCompanyAndDate(filters["partnerId"],min_date,max_date)
              # print("query_outlets")
            
            # datasets = [
            #   {
            #     "label": "Salidas de mineral",
            #     "data": d,
            #     "fill": False,
            #     "borderColor": 'rgb(75, 192, 192)',
            #     "tension": 0.5
            #   }
            # ]
            data = {
              "labels": str_total_days,
              "datasets": datasets
            }
            print(data)

            # print(data)
            res["data"] = data
            res["legend"] = title
            res["success"] = True
            return res, 200
        except Exception as e:
          print(e)
          res["success"] = False
          res["msg"] = "Algio salió mal al obtener el reporte"
          return res, 500

outlet_dataset = api.parser()
outlet_dataset.add_argument("date1", type=inputs.datetime_from_iso8601, required=True, help="Max value is the current date. Example: 2020-06-10")
outlet_dataset.add_argument("date2", type=inputs.datetime_from_iso8601, required=True, help="Max value is the current date. Example: 2020-07-01")
# outlet_dataset.add_argument("companyId", type=str, required=False, help="Company ID. Example: 101293-1230123,10239-1923,12312-21323")

@api.route('/outlet/dataset/')
class AdminOutletDatasetReports(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.doc(security="CmApiKey")
    @api.expect(outlet_dataset, validate=True)
    @jwt_required()
    def get(self):
        '''Get ore outlet dataset report'''
        try:
            res = { "success": False }
            filters = outlet_dataset.parse_args()

            # get all dates between 2 dates
            def fillDates(start, end):
              delta = end - start
              days = [start + timedelta(days = i) for i in range(delta.days + 1)]
              return days

            total_days = fillDates(filters["date1"], filters["date2"])
            # print(total_days)
            str_total_days = []

            # get data for datasests
            queryResult = CmOreOutlet.CmOreOutlet.outletByDate(filters["date1"], filters["date2"])
            # print(queryResult)
            result_array = [[],[]]
            for q in queryResult:
              # print(q[0])
              result_array[0].append(q[0].strftime("%Y-%m-%d"))
              result_array[1].append(q[1])
            # print(result_array)
              # if q[0].strftime("%Y-%m-%d") in str_total_days:
                # print('exist')
                # data.append(q[1])
            d = []
            ## ##
            for t in total_days:
              str_total_days.append(t.strftime("%Y-%m-%d"))
              if t.strftime("%Y-%m-%d") in result_array[0]:
                d.append(result_array[1][result_array[0].index(t.strftime("%Y-%m-%d"))])
                # print(result_array[0].index(t.strftime("%Y-%m-%d")))
              else:
                d.append(0)
            # print(d)
            datasets = [{
              "label": "Salidas de mineral",
              "data": d,
              "fill": False,
              "borderColor": 'rgb(75, 192, 192)',
              "tension": 0.5
            }]
            data = {
              "labels": str_total_days,
              "datasets": datasets
            }

            # res["labels"] = str_total_days
            # res["datasets"] = datasets
            res["data"] = data
            res["success"] = True
            return res, 200
        except Exception as e:
          print(e)
          res["success"] = False
          res["msg"] = "Algio salió mal al obtener el reporte"
          return res, 500

@api.route('/cards/')
class AdminOutletDatasetReports(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.doc(security="CmApiKey")
    @jwt_required()
    def get(self):
        '''Get ore outlet dataset report'''
        try:
            res = { "success": False }
            nComp = CmCompany.CmCompany.countCompany()
            nPart = CmPartner.CmPartner.countPartner()
            nOut = CmOreOutlet.CmOreOutlet.countOutlet()
            nVeh = CmVehicle.CmVehicle.countVehicle()
            nOtd = CmOreOutlet.CmOreOutlet.countOutletToday()

            locNow = datetime.now()
            locfirst = datetime(int(locNow.strftime("%Y")), int(locNow.strftime("%m")), 1)
            # date1 = locNow
            # date2 = 
            # otd = CmOreOutlet.CmOreOutlet.monthAverage(locFirst, locnow)
            # print(otd)

            # get all dates between 2 dates
            def fillDates(start, end):
              delta = end - start
              days = [start + timedelta(days = i) for i in range(delta.days + 1)]
              return days

            total_days = fillDates(locfirst, locNow)
            # print(total_days)
            str_total_days = []

            # get data for datasests
            locnow = locNow.strftime("%Y-%m-%d")
            locFirst = locfirst.strftime("%Y-%m-%d")
            print(locFirst)
            print(locnow)
            queryResult = CmOreOutlet.CmOreOutlet.monthAverage(locFirst, locnow)
            print(queryResult)
            result_array = [[],[]]
            for q in queryResult:
              # print(q[0])
              result_array[0].append(q[0].strftime("%Y-%m-%d"))
              result_array[1].append(q[1])
            # print(result_array)
              # if q[0].strftime("%Y-%m-%d") in str_total_days:
                # print('exist')
                # data.append(q[1])
            d = []
            ## ##
            for t in total_days:
              str_total_days.append(t.strftime("%Y-%m-%d"))
              if t.strftime("%Y-%m-%d") in result_array[0]:
                d.append(result_array[1][result_array[0].index(t.strftime("%Y-%m-%d"))])
                # print(result_array[0].index(t.strftime("%Y-%m-%d")))
              else:
                d.append(0)

            def Average(l): 
              avg = sum(l) / len(l) 
              return avg
            # print(d)
            # av1 = round(Average(d), 1)
            # print(av1)
            if (int(locNow.strftime("%d")) != 1):
              d.pop()
              print("pop")
            # else:
            print(d)
            av = round(Average(d), 1)
            print(av)
            # print(nPart[0][0])
            # print(nOut[0][0])
            # print(nVeh[0][0])
            dashData = {
              "Companies": nComp[0][0],
              "Partners": nPart[0][0],
              "Outlets": nOut[0][0],
              "Vehicles": nVeh[0][0],
              "TodayOut": nOtd[0][0],
              "Average": av
            }

            total_outlets = CmOreOutlet.CmOreOutlet.totalOutlets()
            print(total_outlets)

            companyList = CmOreOutlet.CmOreOutlet.getGroupByCompany()
            # print(companyList)
            compList = []
            for cl in companyList:
              compList.append({
                "id": cl[0].__str__(),
                "name": cl[1],
                "total": cl[2],
                "percentages": round(round(int(cl[2]) / int(total_outlets), 2) * 100, 0)
              })
            # print(compList)
            partnerList = CmOreOutlet.CmOreOutlet.getGroupByPartner()
            partList = []
            for cl in partnerList:
              partList.append({
                "id": cl[0].__str__(),
                "name": cl[1] + " " + cl[2],
                "total": cl[3],
                "percentages": round(round(int(cl[3]) / int(total_outlets), 2) * 100, 0)
              })

            res["data"] = dashData
            res["outletCompany"] = compList
            res["outletPartner"] = partList
            res["success"] = True
            return res, 200
        except Exception as e:
          print(e)
          res["success"] = False
          res["msg"] = "Algio salió mal al obtener el reporte"
          return res, 500

@api.route('/search/partner/<search>')
class AdminOutletSearchPartner(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.doc(params={"search": "search partner"})
    # @api.doc(security="CmApiKey", params={"search": "search partner"})
    # @jwt_required()
    def get(self, search):
        '''Search by partner'''
        try:
            res = { "success": False }
            total_outlets = CmOreOutlet.CmOreOutlet.totalOutlets()
            
            # print(compList)
            partnerList = CmOreOutlet.CmOreOutlet.searchOutletPartner(search)
            print(partnerList)
            partList = []
            for cl in partnerList:
              partList.append({
                "id": cl[0].__str__(),
                "name": cl[1] + " " + cl[2],
                "total": cl[3],
                "percentages": round(round(int(cl[3]) / int(total_outlets), 2) * 100, 0)
              })
            
            res["outletPartner"] = partList
            res["success"] = True
            return res, 200
        except Exception as e:
          print(e)
          res["success"] = False
          res["msg"] = "Algio salió mal al buscar el socio"
          return res, 500

@api.route('/search/company/<search>')
class AdminOutletSearchCompany(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.doc(params={"search": "search company"})
    # @api.doc(security="CmApiKey", params={"search": "search company"})
    # @jwt_required()
    def get(self, search):
        '''Search by company'''
        try:
            res = { "success": False }
            total_outlets = CmOreOutlet.CmOreOutlet.totalOutlets()
            
            # print(compList)
            companyList = CmOreOutlet.CmOreOutlet.searchOutletCompany(search)
            print(companyList)
            compList = []
            for cl in companyList:
              compList.append({
                "id": cl[0].__str__(),
                "name": cl[1],
                "total": cl[2],
                "percentages": round(round(int(cl[2]) / int(total_outlets), 2) * 100, 0)
              })
            
            res["outletCompany"] = compList
            res["success"] = True
            return res, 200
        except Exception as e:
          print(e)
          res["success"] = False
          res["msg"] = "Algio salió mal al buscar el socio"
          return res, 500

parser = api.parser()
parser.add_argument("companyIds", type=str, action="split", required=False, help="Serie of comapny ID's to get stats from them. Example: 101293-1230123,10239-1923,12312-21323")

@api.route('/filter/company/')
class AdminOutletSearchCompany(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.response(400, "Bad request")
    @api.expect(parser, validate=True)
    @api.doc(params={"search": "search company"})
    # @api.doc(security="CmApiKey", params={"search": "search company"})
    # @jwt_required()
    def get(self, search):
        '''Search by company'''
        try:
            res = { "success": False }
            args = parser.parse_args()
            total_outlets = CmOreOutlet.CmOreOutlet.totalOutlets()
            
            # print(compList)
            companyList = CmOreOutlet.CmOreOutlet.searchOutletCompany(search)
            print(companyList)
            compList = []
            for cl in companyList:
              compList.append({
                "id": cl[0].__str__(),
                "name": cl[1],
                "total": cl[2],
                "percentages": round(round(int(cl[2]) / int(total_outlets), 2) * 100, 0)
              })
            
            res["outletCompany"] = compList
            res["success"] = True
            return res, 200
        except Exception as e:
          print(e)
          res["success"] = False
          res["msg"] = "Algio salió mal al buscar el socio"
          return res, 500

    # @api.response(500, "Internal error")
    # @api.response(200, "Success")
    # @api.response(404, "Not found")
    # @api.response(400, "Bad request")
    # @api.expect(partner, validate=True)
    # @api.doc('AddPartner')
    # @api.doc(security="CmApiKey")
    # @jwt_required()
    # def post(self):
    #     '''Add new partner'''
    #     try:
    #         res = { 'success': False }
    #         req = request.get_json()
    #         print(req)
    #         partner = CmPartner.CmPartner.createPartner(req)
    #         res["partner"] = req
    #         res["msg"] = "Se agrego correctamente al socio"
    #         res["success"] = True
    #         return res, 200
    #     except Exception as e:
    #         print(e)
    #         res["success"] = False
    #         res["msg"] = "Algo salió mal al agregar al socio: {0}. Por favor inténtelo nuevamente".format(e)
    #         return res, 500
