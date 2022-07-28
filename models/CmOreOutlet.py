import uuid
from sqlalchemy import or_, and_, desc, text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID, BIGINT, ARRAY
from sqlalchemy.exc import IntegrityError
from models.database import db
from datetime import datetime
from .CmCompany import CmCompany
from .CmPartner import CmPartner

class CmOreOutlet(db.Model):
    '''
    Ore outlet table
    '''

    __tablename__ = "cm_ore_outlet"

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    date = db.Column(db.Date, nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=False)
    section = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    material_type = db.Column(db.Text, nullable=False)
    # minerals = db.Column(db.Text, nullable=False)
    minerals = db.Column(ARRAY(db.String), nullable=True)
    state = db.Column(db.Boolean, nullable = False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    cm_partner_id = db.Column(UUID(as_uuid=True), db.ForeignKey("cm_partner.id"), nullable = True)
    cm_partner = db.relationship("CmPartner", foreign_keys=[cm_partner_id])

    cm_company_id = db.Column(UUID(as_uuid=True), db.ForeignKey("cm_company.id"), nullable = True)
    cm_company = db.relationship("CmCompany", foreign_keys=[cm_company_id])

    cm_driver_id = db.Column(UUID(as_uuid=True), db.ForeignKey("cm_driver.id"), nullable = True)
    cm_driver = db.relationship("CmDriver", foreign_keys=[cm_driver_id])

    cm_vehicle_id = db.Column(UUID(as_uuid=True), db.ForeignKey("cm_vehicle.id"), nullable = True)
    cm_vehicle = db.relationship("CmVehicle", foreign_keys=[cm_vehicle_id])

    cm_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("cm_user.id"), nullable = True)
    cm_user = db.relationship("CmUser", foreign_keys=[cm_user_id])

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception("No se pudo crear la salida de mineral, intente nuevamente") 

    def _id(self):
        return self.id.__str__()

    def createOreOutlet(data):
        try:
            new_ore_outlet = CmOreOutlet(
                date = data['date'],
                number = data['number'],
                section = data['section'],
                quantity = data['quantity'],
                weight = data['weight'],
                material_type = data['materialType'],
                minerals = data['minerals'],
                cm_partner_id = data['partnerId'],
                cm_company_id = data['companyId'],
                cm_driver_id = data['driverId'],
                cm_vehicle_id = data['vehicleId'],
                cm_user_id = data['userId'],
            )
            db.session.add(new_ore_outlet)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("OreOutlet not created")
            raise Exception(e)

    def getAll():
        try:
            return CmOreOutlet.query.all()
        except Exception as e:
            db.session.rollback()
            print("Ore Outlets not found")
            raise Exception(e)

    def oreOutletByCompany(company_id, min_date, max_date):
        try:
            return CmOreOutlet.query.filter(
                CmOreOutlet.cm_company_id == company_id,
                CmOreOutlet.date <= max_date,
                CmOreOutlet.date >= min_date
                ).all()
        except Exception as e:
            db.session.rollback()
            print("Error in report")
            raise Exception(e)

    def oreOutletByPartner(partner_id, min_date, max_date):
        try:
            return CmOreOutlet.query.filter(
                CmOreOutlet.cm_partner_id == partner_id,
                CmOreOutlet.date <= max_date,
                CmOreOutlet.date >= min_date
                ).all()
        except Exception as e:
            db.session.rollback()
            print("Error in report")
            raise Exception(e)

    # def outletPartnerByDate(partner_id, min_date, max_date):
    #     try:
    #         return db.session.query(CmOreOutlet.date, func.count(CmOreOutlet.date)).group_by(CmOreOutlet.date).filter(CmOreOutlet.cm_partner_id == partner_id,CmOreOutlet.date <= max_date, CmOreOutlet.date >= min_date).all()
    #     except Exception as e:
    #         db.session.rollback()
    #         print("Error in query")
    #         raise Exception(e)

    def oreOutletByPartnerList(partner_id):
        try:
            return CmOreOutlet.query.filter(
                CmOreOutlet.cm_partner_id == partner_id
                ).all()
        except Exception as e:
            db.session.rollback()
            print("Error in report")
            raise Exception(e)

    # @classmethod
    def outletByDate(min_date, max_date):
        try:
            return db.session.query(CmOreOutlet.date, func.count(CmOreOutlet.date)).group_by(CmOreOutlet.date).filter(CmOreOutlet.date <= max_date, CmOreOutlet.date >= min_date).all()
        except Exception as e:
            db.session.rollback()
            print("Error in query")
            raise Exception(e)

    def countOutlet():
        try:
            return db.session.query(func.count(CmOreOutlet.id)).all()
        except Exception as e:
            db.session.rollback()
            print("Outlet not found")
            raise Exception(e)

    def countOutletToday():
        try:
            locnow = datetime.now()
            locnow = locnow.strftime("%Y-%m-%d")
            return db.session.query(func.count(CmOreOutlet.id)).filter(CmOreOutlet.date == locnow).all()
        except Exception as e:
            db.session.rollback()
            print("Outlet not found")
            raise Exception(e)

    def monthAverage(min_date, max_date):
        try:
            return db.session.query(CmOreOutlet.date, func.count(CmOreOutlet.date)).group_by(CmOreOutlet.date).filter(CmOreOutlet.date <= max_date, CmOreOutlet.date >= min_date).all()
            # return db.session.query(func.count(CmOreOutlet.id)).filter(CmOreOutlet.date == locnow).all()
        except Exception as e:
            db.session.rollback()
            print("Outlet not found")
            raise Exception(e)

    def getGroupByCompany():
        try:
            return db.session.query(CmOreOutlet.cm_company_id, CmCompany.name, func.count(CmOreOutlet.cm_company_id).label("total_outlets")).join(CmCompany, CmOreOutlet.cm_company_id==CmCompany.id).group_by(CmOreOutlet.cm_company_id, CmCompany.name).order_by(desc("total_outlets")).all()
        except Exception as e:
            db.session.rollback()
            print("Query failed")
            raise Exception(e)

    def getGroupByPartner():
        try:
            return db.session.query(CmOreOutlet.cm_partner_id, CmPartner.name, CmPartner.lastname, func.count(CmOreOutlet.cm_partner_id).label("total_outlets")).join(CmPartner, CmOreOutlet.cm_partner_id==CmPartner.id).group_by(CmOreOutlet.cm_partner_id, CmPartner.name, CmPartner.lastname).order_by(desc("total_outlets")).all()
        except Exception as e:
            db.session.rollback()
            print("Query failed")
            raise Exception(e)

    def searchOutletPartner(name):
        try:
            return db.session.query(CmOreOutlet.cm_partner_id, CmPartner.name, CmPartner.lastname, func.count(CmOreOutlet.cm_partner_id).label("total_outlets")).join(CmPartner, CmOreOutlet.cm_partner_id==CmPartner.id).filter(CmPartner.name.ilike('%{0}%'.format(name))).group_by(CmOreOutlet.cm_partner_id, CmPartner.name, CmPartner.lastname).order_by(desc("total_outlets")).all()
        except Exception as e:
            db.session.rollback()
            print("Query failed")
            raise Exception(e)

    def searchOutletCompany(name):
        try:
            return db.session.query(CmOreOutlet.cm_company_id, CmCompany.name, func.count(CmOreOutlet.cm_company_id).label("total_outlets")).join(CmCompany, CmOreOutlet.cm_company_id==CmCompany.id).filter(CmCompany.name.ilike('%{0}%'.format(name))).group_by(CmOreOutlet.cm_company_id, CmCompany.name).order_by(desc("total_outlets")).all()
        except Exception as e:
            db.session.rollback()
            print("Query failed")
            raise Exception(e)

    def totalOutlets():
        try:
            total = db.session.query(func.count(CmOreOutlet.id)).first()
            return total[0]
        except Exception as e:
            db.session.rollback()
            print("Query failed")
            raise Exception(e)

    def outletByCompanyAndDate(company_id, min_date, max_date):
        try:
            return db.session.query(CmOreOutlet.date, func.count(CmOreOutlet.date).label("outlets")).filter(
                CmOreOutlet.cm_company_id == company_id,
                CmOreOutlet.date <= max_date,
                CmOreOutlet.date >= min_date
                ).group_by(CmOreOutlet.date).order_by(desc(CmOreOutlet.date)).all()
        except Exception as e:
            db.session.rollback()
            print("Error in report")
            raise Exception(e)

    def outletByPartnerAndDate(partner_id, min_date, max_date):
        try:
            return db.session.query(CmOreOutlet.date, func.count(CmOreOutlet.date).label("outlets")).filter(
                CmOreOutlet.cm_partner_id == partner_id,
                CmOreOutlet.date <= max_date,
                CmOreOutlet.date >= min_date
                ).group_by(CmOreOutlet.date).order_by(desc(CmOreOutlet.date)).all()
        except Exception as e:
            db.session.rollback()
            print("Error in report")
            raise Exception(e)
        
    def deleteRows():
        try:
            selecUery = CmOreOutlet.query.limit(1000).all()
            el = []
            for o in selecUery:
                el.append(o._id())
            print("query")
            print(el)
            deleteQuery = CmOreOutlet.__table__.delete().where(CmOreOutlet.id.in_(el))
            db.engine.execute(deleteQuery)
            # db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Error in delete")
            raise Exception(e)

    def getMineralstByDay(date):
        try:
            return db.session.query(func.unnest(CmOreOutlet.minerals).label("outlet_minerals"), func.count(CmOreOutlet.minerals)).filter(CmOreOutlet.date == date).group_by("outlet_minerals").all()
        except Exception as e:
            db.session.rollback()
            print("Error in get ore outlet by day")
            raise Exception(e)
    
    def getMineralstByMonth(date1, date2):
        try:
            return db.session.query(func.unnest(CmOreOutlet.minerals).label("outlet_minerals"), func.count(CmOreOutlet.minerals)).filter(CmOreOutlet.date >= date1, CmOreOutlet.date < date2).group_by("outlet_minerals").all()
        except Exception as e:
            db.session.rollback()
            print("Error in get ore outlet by month")
            raise Exception(e)

    def comparativePerDay(date1, date2):
        try:
            return db.session.query(CmOreOutlet.date, func.count(CmOreOutlet.date)).filter(CmOreOutlet.date >= date1, CmOreOutlet.date <= date2).group_by(CmOreOutlet.date).order_by(CmOreOutlet.date).all()
        except Exception as e:
            db.session.rollback()
            print("Error in comparative by day")
            raise Exception(e)

    def comparativePerMonth(date1, date2):
        try:
            return db.session.query(func.date_trunc("month", CmOreOutlet.date).label("month"), func.count(CmOreOutlet.date)).filter(CmOreOutlet.date >= date1, CmOreOutlet.date < date2).group_by("month").order_by("month").all()
        except Exception as e:
            db.session.rollback()
            print("Error in comparative by month")
            raise Exception(e)

    def weightPerDay(date1, date2):
        try:
            return db.session.query(CmOreOutlet.date, func.sum(CmOreOutlet.weight)).filter(CmOreOutlet.date >= date1, CmOreOutlet.date <= date2).group_by(CmOreOutlet.date).order_by(CmOreOutlet.date).all()
        except Exception as e:
            db.session.rollback()
            print("Error in weight by day")
            raise Exception(e)

    def weightPerMonth(date1, date2):
        try:
            return db.session.query(func.date_trunc("month", CmOreOutlet.date).label("month"), func.sum(CmOreOutlet.weight)).filter(CmOreOutlet.date >= date1, CmOreOutlet.date < date2).group_by("month").order_by("month").all()
        except Exception as e:
            db.session.rollback()
            print("Error in weight by month")
            raise Exception(e)