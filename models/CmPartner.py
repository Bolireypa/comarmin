import uuid
from sqlalchemy import or_, and_, desc, text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID, BIGINT
from sqlalchemy.exc import IntegrityError
from models.database import db
from datetime import datetime

class CmPartner(db.Model):
    '''
    Partner table
    '''

    __tablename__ = "cm_partner"

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    name = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    ci = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, unique=True, nullable=True)
    membership_date = db.Column(db.Date, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=True)
    cellphone = db.Column(db.Integer, unique=True, nullable=False)
    state = db.Column(db.Boolean, nullable = False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            raise Exception('No se pudo crear al socio, intente nuevamente')
        except Exception as e:
            db.session.rollback()
            raise Exception('No se pudo crear al socio, intente nuevamente')

    def _id(self):
        return self.id.__str__()

    def createPartner(data):
        try:
            new_partner = CmPartner(
                name = data['name'],
                lastname = data['lastname'],
                ci = data['ci'],
                address = data['address'],
                membership_date = data['membershipDate'],
                cellphone = data['cellphone']
            )
            db.session.add(new_partner)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Partner not created")
            raise Exception(e)

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Partner not updated")
            raise Exception(e) 

    def getAll():
        try:
            return CmPartner.query.all()
        except Exception as e:
            db.session.rollback()
            print("Partners not found")
            raise Exception(e)

    def getById(partner_id):
        try:
            return CmPartner.query.filter(CmPartner.id == partner_id).first()
        except Exception as e:
            db.session.rollback()
            print("Partner not found")
            raise Exception(e)

    def getByFilter(filters, parameter):
        try:
            # if filters == "name":
                return CmPartner.query.filter(CmPartner.name == partner)
        except Exception as e:
            db.session.rollback()
            print("Partner not found")
            raise Exception(e)

    def countPartner():
        try:
            return db.session.query(func.count(CmPartner.id)).all()
        except Exception as e:
            db.session.rollback()
            print("Partner not found")
            raise Exception(e)