import uuid
from sqlalchemy import or_, and_, desc, text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID, BIGINT
from sqlalchemy.exc import IntegrityError
from models.database import db
from datetime import datetime

class CmCompany(db.Model):
    '''
    Company table
    '''

    __tablename__ = "cm_company"

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    name = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    department = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    logo = db.Column(db.Text, nullable=True)
    nit = db.Column(db.Text, nullable=False)
    header = db.Column(db.Text, nullable=True)
    state = db.Column(db.Boolean, nullable = False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def _id(self):
        return self.id.__str__()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            raise Exception('No se pudo crear la empresa, intente nuevamente')
        except Exception as e:
            db.session.rollback()
            raise Exception('No se pudo crear la empresa, intente nuevamente')

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Company not updated")
            raise Exception(e) 

    def createCampany(data):
        try:
            # print("create user function in model", data)
            new_company = CmCompany(
                name = data['name'],
                city = data['city'],
                department = data['department'],
                phone = data['phone'],
                logo = 'url logo',
                nit = data['nit']
            )
            db.session.add(new_company)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Company not created")
            raise Exception(e)

    def getAll():
        try:
            return CmCompany.query.all()
        except Exception as e:
            db.session.rollback()
            print("User not found")
            raise Exception(e)

    def getById(company_id):
        try:
            return CmCompany.query.filter(CmCompany.id == company_id).first()
        except Exception as e:
            db.session.rollback()
            print("Company not found")
            raise Exception(e)

    def countCompany():
        try:
            return db.session.query(func.count(CmCompany.id)).all()
        except Exception as e:
            db.session.rollback()
            print("Company not found")
            raise Exception(e)
