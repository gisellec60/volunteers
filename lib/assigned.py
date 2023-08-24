from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Volunteer, Schedule, Role, volunteer_role

engine = create_engine('sqlite:///volunteers.db')
Session = sessionmaker(bind=engine)
session = Session()

def populate_assign():
     volunteers = session.query(Volunteer).all()
    #  schedules = session.query(Schedule).all()
     for volunteer in volunteers:
        if not volunteer.schedules:
            volunteer.assigned = "No"
            session.commit()
