import uuid
from sqlalchemy import or_, and_, desc, text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID, BIGINT
from sqlalchemy.exc import IntegrityError
from models.database import db
from datetime import datetime

class CmPricing(db.Model):
    '''
    Pricing table
    '''

    __tablename__ = "cm_pricing"

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    ore = db.Column(db.Text, nullable=False)
    percent = db.Column(JSONB, nullable=True)
    pricing = db.Column(JSONB, nullable=False)
    pricing_ton = db.Column(JSONB, nullable=True)
    short = db.Column(db.Text, nullable=False)
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
        except: 
            db.session.rollback()
            raise Exception("Failed to save Pricing")

    def createPricing(data):
        try:
            # print("create user function in model", data)
            new_pricing = CmPricing(
              ore = data['ore'],
              pricing = {'ore': data['short'], 'pricing': data['pricing']},
              short = data['short']
            )
            db.session.add(new_pricing)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Pricing not created")
            raise Exception(e)

    def getAll():
        try:
            return CmPricing.query.order_by(desc(CmPricing.ore)).all()
        except Exception as e:
            db.session.rollback()
            print("Pricing not found")
            raise Exception(e)

    def getById(pricing_id):
        try:
            return CmPricing.query.filter(CmPricing.id == pricing_id).first()
        except Exception as e:
            db.session.rollback()
            print("Pricing not found")
            raise Exception(e)

    # def countCompany():
    #     try:
    #         return db.session.query(func.count(CmCompany.id)).all()
    #     except Exception as e:
    #         db.session.rollback()
    #         print("Company not found")
    #         raise Exception(e)
