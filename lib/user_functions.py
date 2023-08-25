
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import Volunteer, Validate
from prettycli import red

engine = create_engine('sqlite:///volunteers.db')
Session = sessionmaker(bind=engine)
session = Session()

def username_input():
        username = input("\nEnter the username or x to quit: ")
        username = username.strip()
        return username     

def clear_screen():
        print("\n" * 40)

def user_exist(username):
        volunteer = session.query(Volunteer).filter(Volunteer.username==username).first() 
        return volunteer 

def keep_output_on_screen():
        user_input = input("\nEnter to exit: ") 
        return user_input

def get_volunteer_information(field, input_message, error_message):
    loop = True
    while loop:
        field_input = input(input_message)
        if field_input == "X" or field_input == "x":
            break
        else:
            field_valid = Validate.validate_get_volunteer_information(field, field_input)
            if not field_valid :
               print(red(error_message))
               field_input = input("\nHit enter to try again or x to quit: ")
               if field_input.upper() == "X":
                    loop = False
                    break
               else:
                    continue
            else:
                if field == "floater":    
                   field = True if field_input == 'Y' else False
                   field_input = field
                loop = False 

    return field_input   