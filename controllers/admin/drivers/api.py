from flask_restx import Namespace

api = Namespace("admin_drivers", description="Manage drivers")

from .AdminDrivers import AdminDrivers