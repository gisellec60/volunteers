#!/usr/bin/env python3

from sqlalchemy import create_engine, exc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from model import   Volunteer, Role, Schedule, join_table
import click
import re
import ipdb; ipdb.set_trace()
from datetime import datetime, date

# @click.command()
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name', help='The person to greet.')
Base = declarative_base()

class Validate(Base):
    name_error_message="First and last name must consist of A-z ,-,'."
    email_error_message="Please enter a valid email"
    phone_error_message="Please enter a valid phone number"
    role_error_message="role contains only A-z. Please enter a valid role"
    role_exist_error_message="role does not exist"
    user_exist_error_message="username does not exist"
    floater_error_message="Floater value: True or False"
    week_error_message="Week must be an integer 1-5"
    date_error_message=f"Please enter a valid date: 2023-08-17. Note date cannot be before {date.today()}"
    
    def validate_name(fname, lname, name_error_message):
        name_pattern =  r"[A-z'-]+$"
        regex = re.compile(name_pattern)
        match = regex.fullmatch(fname)

        if match == None:
           raise Exception(name_error_message)  
        else:   
           match = regex.fullmatch(lname)   
           if match == None:
              raise Exception(name_error_message)    

    def validate_email(email, email_error_message):
        email_pattern = r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$"
        regex = re.compile(email_pattern)
        match = regex.fullmatch(email)
        if match == None:
            raise Exception(email_error_message)  

    def validate_phone(phone,phone_error_message):
        phone_pattern = r"[\d\d\d-\d\d\d-\d\d\d\d]"
        regex = re.compile(phone_pattern)
        match = regex.fullmatch(phone)
        if match == None:
           raise Exception(phone_error_message)

    def validate_role_exist(role):
        valid_role = session.query(Role).filter(Role.position == role).one()
        # except exc.SQLAlchemyError as e:
        # print(type(e))
    
    def validate_role(role, role_error_message):
        role_pattern =  r"[A-z]+$" 
        regex = re.compile(role_pattern)   
        match = regex.fullmatch(role)   
        if match == None:
            raise Exception(role_error_message)

    def validate_floater(floater, floater_error_message):
        if floater != "True" and floater != "False":
            raise Exception(floater_error_message)
    
    def validage_week(week, week_error_message):
        week_pattern = r"[1-5]"
        regex = re.compile(week_pattern)
        match = regex.fullmatch(week)
        if match == None:
            raise Exception(week_error_message)

    def validate_volunteer_exist(username):
        valid_username = session.query(Volunteer).filter(Volunteer.username == username).one()
        # except exc.SQLAlchemyError as e:
        # print(type(e))

    def validate_date(date, date_error_message):
        schedule_date = datetime.strptime(date, '%Y-%m-%d').date()
        schedule_date_pattern = r"^2023(0[89]|1[012])(0[1-9]|[12][0-9]|3[01])$"
        regex = re.compile(schedule_date_pattern)
        match = regex.fullmatch(schedule_date)
        if match:
            today = date.today()
            if today >  schedule_date:
                raise Exception("Date must be current or future")
        else:
            raise Exception(date_error_message)   

def start():
    import ipdb; ipdb.set_trace()
    print("Welcome to Schedulier \n")
    print("Add Volunteer")
    print("Delete Volunteer")
    user_input = input("Pick one")

    handle_user_input(user_input)

    def handle_user_input(input):
        import ipdb; ipdb.set_trace()
        is_number = input.isdigit()
        if is_number:
           handle_add_volunteer(input)

    def handle_add_volunteer():
        pass

if __name__ == '__main__':
    engine = create_engine('sqlite:///volunteers.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    hello()

    