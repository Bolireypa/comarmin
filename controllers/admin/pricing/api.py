from flask_restx import Namespace

api = Namespace("admin_pricing", description="Manage pricing")

from .AdminPricing import AdminPricing