import re
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///volunteers.db')
Session = sessionmaker(bind=engine)
session = Session()

class Validate():
   
    def validate_name(name):
        name_pattern =  r"[A-z'-]+$"
        regex = re.compile(name_pattern)
        match = regex.fullmatch(name)
        return match

    def validate_email(email):
        email_pattern = r"^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,}\b"
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
        
    def validate_fields(field):
            valid_fields = ["first_name", "last_name", "email", "phone","floater","week","role"]  
            if field in valid_fields:
                return True    
           
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
        schedule_date_pattern = r"^202[3-9]-(0[9,4,6]|1[1])-(0[1-9]|[1,2][0-9]|3[0])|^202[3-9]-(0[1,3,5,7,8]|1[0,2])-(0[1-9]|[1,2][0-9]|3[1])$"
        regex = re.compile(schedule_date_pattern)
        match = regex.fullmatch(date)
        return match

    def username_input():
        username = input("\nEnter the username or x to quit: ")
        username = username.strip()
        return username     
    

    def keep_output_screen():
        user_input = input("x to exit: ") 
        user_input = user_input.strip()     
        return user_input