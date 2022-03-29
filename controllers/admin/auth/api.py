from flask_restx import Namespace

api = Namespace("admin_login", description="Login")

from .AdminAuth import AdminAuth