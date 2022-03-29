from flask_restx import Namespace

api = Namespace("admin_vehicles", description="Manage vehicles")

from .AdminVehicles import AdminVehicles