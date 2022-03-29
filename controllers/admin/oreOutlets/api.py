from flask_restx import Namespace

api = Namespace("admin_ore_outlets", description="Manage ore outlets")

from .AdminOreOutlets import AdminOreOutlets