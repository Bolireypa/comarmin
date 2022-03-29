from flask_restx import Namespace

api = Namespace("admin_reports", description="Get reports")

from .AdminReports import AdminReports