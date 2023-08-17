from datetime import datetime, date
import re
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

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
    
    def validate_role_exist(role):
        valid_role = session.query(Role).filter(Role.position == role).one()
        # except exc.SQLAlchemyError as e:
        # print(type(e))
    
    def validate_role(role):
        role_pattern =  r"[A-z]+$" 
        regex = re.compile(role_pattern)   
        match = regex.fullmatch(role)  
        return match 
    
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
        schedule_date_pattern = r"^2023-(0[1-9]|1[1,2])-(0[1-9]|[12][0-9]|3[01])$"
        regex = re.compile(schedule_date_pattern)
        match = regex.fullmatch(date)
        return match
        