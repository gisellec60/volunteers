from datetime import datetime, date
import re
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# from model import Volunteer, Role, Schedule

engine = create_engine('sqlite:///volunteers.db')
Session = sessionmaker(bind=engine)
session = Session()

class Validate():
    name_error_message="First and last name must consist of A-z ,-,'."
    email_error_message="Please enter a valid email"
    phone_error_message="Please enter a valid phone number"
    role_error_message="role contains only A-z. Please enter a valid role"
    role_exist_error_message="role does not exist"
    user_exist_error_message="username does not exist"
    floater_error_message="Floater value: True or False"
    week_error_message="Week must be an integer 1-5"
    date_error_message=f"Please enter a valid date: Note date cannot be before {date.today()}"
    
    def validate_name(name):
        name_pattern =  r"[A-z'-]+$"
        regex = re.compile(name_pattern)
        match = regex.fullmatch(name)
        return match

    def validate_email(email):
        email_pattern = r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"
        regex = re.compile(email_pattern)
        match = regex.fullmatch(email)
        return match

    def validate_phone(phone):
        phone_pattern = r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$"
        regex = re.compile(phone_pattern)
        match = regex.fullmatch(phone)
        return match
            
    def validate_role_input(role):
        role_pattern =  r"[A-z]+$" 
        regex = re.compile(role_pattern)   
        match = regex.fullmatch(role)  
        return match 

    def validate_role(role):
        user_roles = ["greeter","usher","welcome table", "prayer"]   
        if role in user_roles:
            return True
           
    def list_volunteer_roles(username,role):
        role_list=[]
        volunteer = session.query(Volunteer).filter(Volunteer.username == username)
        for role in volunteer.roles:
           role_list.append(role.position)
        return role_list        
    
    def list_volunteer_schedules(username,date):
        schedule_date = datetime.strptime(date, '%Y-%m-%d').date()
        schedule_list = []
        volunteer = session.query(Volunteer).filter(Volunteer.username == username)
        for schedule in volunteer.schedules:
            if schedule.date == schedule_date:
               schedule_list.append(schedule)
        return schedule_list
     
    def user_exist(username):
        volunteer = session.query(Volunteer).filter(Volunteer.username==username).first() 
        return volunteer
    
    def validate_floater(floater):
        floater_is_good = "Yes"
        if floater != True and floater != False:
           floater_is_good = "No" 
        return floater_is_good
            
    
    def validate_week(week):
        week_pattern = r"[1-5]"
        regex = re.compile(week_pattern)
        match = regex.fullmatch(week)
        return match
    
    def validate_date(date):
        # schedule_date = datetime.strptime(date, '%Y-%m-%d').date()
        # schedule_date_pattern = r"^202[3-9]-(0[1-9]|1[1,2])-(0[1-9]|[12][0-9]|3[01])$"
        schedule_date_pattern = r"^202[3-9]-(0[9,4,6]|[11])-(0[1-9]|[12][0-9]|3[0])|^202[3-9]-(0[1,3,5,7,8]|1[0,2])-(0[1-9]|[1,2][0-9]|3[1])$"
        regex = re.compile(schedule_date_pattern)
        match = regex.fullmatch(date)
        return match
         