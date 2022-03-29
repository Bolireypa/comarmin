from flask_restx import Api
from flask import Blueprint

blueprint = Blueprint('api_v1', __name__, url_prefix="/api/v1")

auth = {
    "CmApiKey": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "**'Bearer &lt;JWT&gt;'** in the textbox"
    },
}

api = Api(
  blueprint,
  title='App title',
  version='1.0',
  description='Admin module API`s ',
  authorizations=auth
)

from controllers.admin.auth.api import api as admin_ns1
from controllers.admin.users.api import api as admin_ns2
from controllers.admin.companies.api import api as admin_ns3
from controllers.admin.partners.api import api as admin_ns4
from controllers.admin.drivers.api import api as admin_ns5
from controllers.admin.vehicles.api import api as admin_ns6
from controllers.admin.oreOutlets.api import api as admin_ns7
from controllers.admin.reports.api import api as admin_ns8
from controllers.admin.pricing.api import api as admin_ns9

api.add_namespace(admin_ns1, path="/login")
api.add_namespace(admin_ns2, path="/users")
api.add_namespace(admin_ns3, path="/companies")
api.add_namespace(admin_ns4, path="/partners")
api.add_namespace(admin_ns5, path="/drivers")
api.add_namespace(admin_ns6, path="/vehicles")
api.add_namespace(admin_ns7, path="/ore_outlets")
api.add_namespace(admin_ns8, path="/reports")
api.add_namespace(admin_ns9, path="/pricing/table")