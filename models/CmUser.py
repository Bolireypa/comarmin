import uuid
from sqlalchemy import or_, and_, desc, text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID, BIGINT
from sqlalchemy.exc import IntegrityError
from models.database import db
from datetime import datetime

class CmUser(db.Model):
  '''
  User table
  '''

  __tablename__ = "cm_user"

  id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
  name = db.Column(db.Text, nullable=False)
  lastname = db.Column(db.Text, nullable=False)
  email = db.Column(db.String(70), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)
  birth_date = db.Column(db.Date, nullable=True)
  phone = db.Column(db.Integer, unique=True, nullable=True)
  cellphone = db.Column(db.Integer, unique=True, nullable=False)
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
        raise Exception('No se pudo crear al usuario, intente nuevamente')
    except Exception as e:
        db.session.rollback()
        raise Exception('No se pudo crear al usuario, intente nuevamente')

  def update(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Company not updated")
            raise Exception(e) 

  def createUser(data):
    try:
      print("create user function in model", data)
      new_user = CmUser(
        name = data['name'],
        lastname = data['lastname'],
        email = data['email'],
        password = data['password'],
        birth_date = data['birthDate'],
        cellphone = data['cellphone']
      )
      db.session.add(new_user)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      print("User not created")
      raise Exception(e)

  def getUsers():
    try:
      return CmUser.query.all()
    except Exception as e:
      db.session.rollback()
      print("User not found")
      raise Exception(e)

  def getUserByEmail(email):
    try:
      return CmUser.query.filter(CmUser.email == email).first()
    except Exception as e:
      db.session.rollback()
      print("User not found")
      raise Exception(e)

  def getById(user_id):
    try:
        return CmUser.query.filter(CmUser.id == user_id).first()
    except Exception as e:
        db.session.rollback()
        print("User not found")
        raise Exception(e)