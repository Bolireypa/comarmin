from flask_restx import Namespace

api = Namespace("admin_companies", description="Manage companies")

from .AdminCompanies import AdminCompanies