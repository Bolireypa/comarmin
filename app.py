from flask import Flask, render_template
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

from models.database import db

import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()
from os import getenv

from config import cors

# def create_app():



# db = SQLAlchemy()

from models import (
    CmUser,
    CmPartner,
    CmCompany,
    CmVehicle,
    CmDriver,
    CmOreOutlet,
    CmPricing
)

from db_data_init import createInitialData

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://icxemeigeagsjp:6f565e2f9b3e3e5c30cc7bc5c6a25ebaac4940915bc4f7897625593984fcefe3@ec2-34-237-46-61.compute-1.amazonaws.com:5432/db4jm1voqc1lnq'
    # app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URI_DEV")

    app.config["JWT_SECRET_KEY"] = getenv("JWT_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

    # class CmUser(db.Model):
    #     id = db.Column(db.Integer, primary_key=True)
    #     username = db.Column(db.String(80), unique=True, nullable=False)
    #     email = db.Column(db.String(120), unique=True, nullable=False)

    #     def __repr__(self):
    #         return '<User %r>' % self.username



    @app.route('/')
    def index():
        return render_template('index.html')
    # class RootHome(Resource):
    #     def get(self):
    #         return {'hello': 'world'}

    CORS(app, origins=cors.origins(), supports_credentials=True)


    # init SQLAlchemy
    db.init_app(app)

    JWTManager(app)

    with app.app_context():
        createInitialData()
        # create tables
        db.create_all()

    @app.teardown_request
    def teardown_request(exception=None):
        if exception:
            db.session.rollback()
        ## flush the db session
        db.session.remove()

    return app, db

app, db = create_app()

# init blueprint
from apis.admin_api import blueprint as blueprintv1

app.register_blueprint(blueprintv1)


# init API`s
# from apis.admin_api import api

# api.init_app(app)

if __name__ == '__main__':
    app.run()