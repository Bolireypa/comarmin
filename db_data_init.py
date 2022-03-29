from models import CmUser
from sqlalchemy_utils import create_database, database_exists
from os import getenv

def createInitialData():
  try:
    create_default_database()
    checkUser = CmUser.CmUser.getUsers()
    if not checkUser:
      user_data = {
        "name": "User",
        "lastname": "One",
        "email": "user@mail.com",
        "password": "password",
        # "username": "zb-root",
        "cellphone": "78451100",
        # "countryCode": "+591",
        # "timezoneOffset": 240,
        "birthDate": "2020-02-10"
      }
      user = CmUser.CmUser.createUser(user_data)
      if user:
        print("user created successfully!!!!!")
  
  except Exception as e:
    print('error creating data')
    print(e)
    print('error creating data')

def create_default_database():
    ## create db if not exists 
    if not database_exists(getenv("DATABASE_URI")):
        create_database(getenv("DATABASE_URI"))
    ## create bugs db
    # if not database_exists(getenv("DATABASE_QA_URI")):
        # create_database(getenv("DATABASE_QA_URI"))