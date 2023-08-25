#!/usr/bin/env python3

from faker import Faker
import random
from random import choice as rc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Volunteer, Schedule, Role, volunteer_role

engine = create_engine('sqlite:///volunteers.db')
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

vol_positions = ['greeter', 'usher', 'welcome table', 'prayer']

def delete_records():
    session.query(Volunteer).delete()
    session.query(Role).delete()
    session.query(Schedule).delete()
    session.query(volunteer_role).delete()
    session.commit()

def create_volunteers():
    volunteers = []
    for _ in range(34):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name}_{last_name}"

        volunteer = Volunteer(
           first_name = first_name, 
           last_name = last_name,  
           email = fake.free_email(),
           phone = fake.phone_number(),
           username = username,
           week = random.randint(1,4),
           floater = fake.boolean(chance_of_getting_true=9),
           assigned = "Yes"
       )
        
        session.add(volunteer)   
        session.commit()  
        volunteers.append(volunteer) 
    return volunteers   

 
def create_roles():
    roles = []
    for vol_position in vol_positions:
        role = Role(
            position = vol_position
        ) 
        session.add(role) 
        session.commit()
        roles.append(role)
    return roles
  
def relate_vol_pos(volunteers,roles):
    for role in roles:
        if role.position != 'prayer':
            for i in range(0,4):
                volunteers[i].roles.append(role)
                session.commit()
                volunteers.pop(i)         
        else:
            volunteers = session.query(Volunteer).all()
            for j in range (10,34):
                volunteers[j].roles.append(role)
                session.commit()


def create_schedules():
    schedules = []
    for _ in range(50):
        schedule = Schedule(
            date = fake.date_this_month(after_today=True),
            swappout_id=""
        ) 
        session.add(schedule) 
        session.commit()
        schedules.append(schedule)
    return schedules    

#Get random volunter scheduled
def populate_schedule(volunteers,schedules):
    for schedule in schedules:
        schedule.vol_id = rc(volunteers)

def add_roles_to_schedule(schedules):
        for schedule in schedules:
            volunteer = session.query(Volunteer).filter(Volunteer.id==schedule.vol_id).first() 
            print('this is volunteer==========================',volunteer)
            for role in volunteer.roles:
                schedule.role_id = role.id

def populate_swappout(schedules):
    for i in range(2,34,5):
        schedules[i].swappout_id = random.randint(1,34)
        session.commit()     

def floater_setting(volunteers):
    for volunteer in volunteers:
        if volunteer.floater:
            volunteer.week = 5
            session.commit()

def populate_assign(volunteers):
     for volunteer in volunteers:
        if not volunteer.schedules:
            volunteer.assigned = "No"
            session.commit()

if __name__ == '__main__':
    delete_records()
    roles = create_roles()
    volunteers = create_volunteers()
    relate_vol_pos(volunteers,roles)
    schedules = create_schedules()
    volunteers,schedules = populate_schedule(volunteers,schedules)
    floater_setting(volunteers)
    populate_assign(volunteers)
    populate_swappout(schedules)