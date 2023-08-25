import re
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
# from model import Volunteer
engine = create_engine('sqlite:///volunteers.db')
Session = sessionmaker(bind=engine)
session = Session()

class Validate():

    fname_input_message="\nEnter first name or x to quit: "
    lname_input_message="\nEnter last name or x to quit: "
    name_error_message="\nFirst and last name can only consist of A-z ,-,'."

    email_error_message="\nPlease enter a valid email"
    email_input_message="\nEnter email or x to quit "

    phone_error_message="\nPlease enter a valid phone number"
    phone_input_message="\nEnter phone number or x to quit: "

    role_error_message="\nrole does not exist"
    role_input_message = "\nEnter a  position [greeter, usher, welcome table, prayer]: "

    user_exist_error_message="\nusername does not exist"

    floater_error_message="\nFloater value: Y or N"
    floater_input_message ="\nIs volunteer a floater? Y/N or x to quit: "

    week_error_message="\nWeek must be an integer 1-5"
    week_input_message="\nEnter week [1-5] x to quit: "

    date_error_message=f"\nPlease enter a valid date: YYY-MM-DD "

    valid_fields = ["first_name", "last_name", "email", "phone","floater","week,role"] 
   
    
    def validate_get_volunteer_information(field, field_input):
        if field == "week":
            if int(field_input) in [1, 2, 3, 4, 5] :
                return True
        elif field == "role":
            if field_input in ["greeter","usher","welcome table", "prayer"]:
                return True
        elif field == "floater":
            if field_input in ['Y','y','n','N']:
                return True    
        elif field == "phone":
            phone_pattern = r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$"
            regex = re.compile(phone_pattern)
            match = regex.fullmatch(field_input)
            return match
        elif field == "email":
            email_pattern = r"^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,}\b"
            regex = re.compile(email_pattern)
            match = regex.fullmatch(field_input)
            return match
        elif field == "fname" or field == "lname":
            name_pattern =  r"[A-z'-]+$"
            regex = re.compile(name_pattern)
            match = regex.fullmatch(field_input)
            return match

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
    
    def clear_screen():
            print("\n" * 40)

    def user_exist(username):
            volunteer = session.query(Volunteer).filter(Volunteer.username==username).first() 
            return volunteer 

    def keep_output_on_screen():
            user_input = input("\nEnter to exit: ") 
            return user_input

    def try_again():
        input("\nEnter email or x to quit: ")
