from flask_restx import Namespace

api = Namespace("admin_users", description="Manage users")

from .AdminUsers import AdminUsers