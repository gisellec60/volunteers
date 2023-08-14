#!/usr/bin/env python3
import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy import Table, Boolean, ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.dialects.sqlite import DATE
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date

engine = create_engine('sqlite:///volunteers.db')
Session = sessionmaker(bind=engine)
session = Session()

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}

metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)
 
volunteer_role = Table (
     'volunteer_role',
     Base.metadata,
     Column('vol_id', ForeignKey('volunteers.id')),
     Column('role_id', ForeignKey('roles.id'))
)

class Volunteer(Base):
    __tablename__ = "volunteers"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True)
    phone = Column(String, nullable=False)
    username = Column(String, unique=True)
    floater = Column (Boolean, nullable=False)
    week = Column(Integer, nullable=False)
    assigned = Column(String, nullable=False)

    roles = relationship('Role', secondary='volunteer_role',
                          back_populates='volunteers')
    schedules = relationship('Schedule', backref=backref('volunteer'))
        
    def __repr__(self):
        return f'Volunteer: {self.id}, ' + \
               f'Fname: {self.first_name}, ' + \
               f'Lname: {self.last_name}, ' + \
               f'Email: {self.email},' + \
               f'Username: {self.username}, ' + \
               f'Floater: {self.floater}, ' + \
               f'Phone: {self.phone}, ' + \
               f'Week : {self.week}, ' + \
               f'Assigned: {self.assigned}' 

    def add_volunteer(fname, lname, email, phone, floater, week, position="prayer"):
            username = f"{fname}_{lname}"
            assigned = "No"  
            role = session.query(Role).filter(Role.position == position).first()
            volunteer = Volunteer(
                     first_name = fname, 
                     last_name = lname,
                     email = email,
                     phone = phone,
                     username = username,
                     floater = floater,
                     week = week,
                     assigned = assigned
            )
            
            volunteer.roles.append(role)
            session.add(volunteer)
            session.commit()
            return volunteer
   
    def delete_volunteer(username):
        volunteer = session.query(Volunteer).filter(
                    Volunteer.username == username).first()
        
        # Delete Volunteer _Role association from volunteer_role table
        [volunteer.roles.remove(role) for role in volunteer.roles]
        
        # Delete volunteer from schedule
        if volunteer.schedules:
            [session.delete(schedule) for schedule in volunteer.schedules]
       
        # Delete Volunteer
        session.delete(volunteer)
        session.commit() 

    def modify_volunteer(username, changes):
        volunteer=session.query(Volunteer).filter(Volunteer.username == username).one()
        for key,value in changes.items():
            setattr(volunteer,key,value)
        session.commit()
    
class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    position = Column(String, nullable=False)

    volunteers = relationship('Volunteer', secondary='volunteer_role',
                          back_populates='roles')
    schedules = relationship('Schedule', backref=backref('role'))
    
    def __repr__(self):
        return f'Role id: {self.id}, ' + \
               f'Position: {self.position} '

    def add_role(role):
        role = Role(
            position = role
        ) 
        session.add(role) 
        session.commit()
        return role  
     
    def del_role(position):
        role = session.query(Role).filter(Role.position == position).one()

        # Delete role from schedule
        if role.schedules:
            [session.delete(schedule) for schedule in role.schedules]

        # Delete Volunteer_Role association from volunteer_role table
        [role.volunteers.remove(volunteer) for volunteer in role.volunteers] 

        # Delete Role
        session.delete(role)
        session.commit() 


class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    date = Column(DATE, nullable=False)
    swappout_id = Column(Integer,nullable=True)

    vol_id = Column(Integer, ForeignKey('volunteers.id'))
    role_id = Column(Integer, ForeignKey('roles.id'))

          
    def add_to_schedule(username,position,input_date):
        
        schedule_date = datetime.strptime(input_date, '%Y-%m-%d').date()

        volunteer = session.query(Volunteer).filter(Volunteer.username == username).one()
        role = session.query(Role).filter(Role.position == position).one()
               
        schedule = Schedule(
            date = schedule_date,
            vol_id = volunteer.id,
            role_id = role.id
        )
        
        session.add(schedule)
        session.commit()

    def delete_schedule(username, input_date):

        schedule_date = datetime.strptime(input_date, '%Y-%m-%d').date()
        volunteer = session.query(Volunteer).filter(Volunteer.username == username).one()
        [session.delete(schedule) for schedule in volunteer.schedules if schedule.date == schedule_date]
        
        session.commit()

    def swap(username, swapname, input_date):
        pass   


    def modify_schedule(username, input_date, role, changes):

        schedule_date = datetime.strptime(input_date, '%Y-%m-%d').date()
        role = session.query(Role).filter(Role.position == "greeter").first()
        volunteer=session.query(Volunteer).filter(Volunteer.username == username).one()
        schedule = session.query(Schedule).filter(Schedule.vol_id == volunteer.id,
               Schedule.date == schedule_date,Schedule.role_id == role.id).one()
        
        for key,value in changes.items():
            if key == "username":
               user = session.query(Volunteer).filter(Volunteer.username == value )
               setattr(schedule.vol_id,key,user.id)
            elif key == "position":
                role = session.query(Role).filter(Role.position == value )
                setattr(schedule.role_id,key,role.id)
            else:
                new_date = datetime.strptime(value, '%Y-%m-%d').date()
                setattr(schedule.date,key,new_date)    
        session.commit()

    def __repr__(self):
        return f'Schedule: {self.id}, ' + \
               f'Swapped: {self.swappout_id}, ' + \
               f'Volunteer: {self.vol_id}, ' + \
               f'Role: {self.role_id}, ' + \
               f'Date: {self.date} '
             
             