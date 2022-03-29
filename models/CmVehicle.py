import uuid
from sqlalchemy import or_, and_, desc, text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID, BIGINT
from sqlalchemy.exc import IntegrityError
from models.database import db
from datetime import datetime

class CmVehicle(db.Model):
    '''
    Vehicle table
    '''

    __tablename__ = "cm_vehicle"

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    vehicle_type = db.Column(db.Text, nullable=False)
    model = db.Column(db.Text, nullable=False)
    license_plate = db.Column(db.Text, nullable=False)
    color = db.Column(db.Text, nullable=False)
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
            raise Exception('No se pudo crear el vehiculo, intente nuevamente')
        except Exception as e:
            db.session.rollback()
            raise Exception('No se pudo crear el vehiculo, intente nuevamente')

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Company not updated")
            raise Exception(e) 

    def _id(self):
        return self.id.__str__()

    def createVehicle(data):
        try:
            new_vehicle = CmVehicle(
                vehicle_type = data['vehicleType'],
                model = data['model'],
                license_plate = data['licensePlate'],
                color = data['color'],
                # color = data['color'],
            )
            db.session.add(new_vehicle)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Vehicle not created")
            raise Exception(e)

    def getAll():
        try:
            return CmVehicle.query.all()
        except Exception as e:
            db.session.rollback()
            print("Vehicles not found")
            raise Exception(e)

    def getById(vehicle_id):
        try:
            return CmVehicle.query.filter(CmVehicle.id == vehicle_id).first()
        except Exception as e:
            db.session.rollback()
            print("Vehicle not found")
            raise Exception(e)

    def countVehicle():
        try:
            return db.session.query(func.count(CmVehicle.id)).all()
        except Exception as e:
            db.session.rollback()
            print("Vehicle not found")
            raise Exception(e)