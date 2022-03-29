from flask_restx import Namespace

api = Namespace("admin_partners", description="Manage partners")

from .AdminPartners import AdminPartners