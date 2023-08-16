#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from model import  Volunteer, Role, Schedule, Validate
import click
import ipdb
from datetime import datetime, date

engine = create_engine('sqlite:///volunteers.db')
Session = sessionmaker(bind=engine)
session = Session()

def add_volunteer():
    x=True
    add_v = False
    while x:
        print ("Add Volunteer")
        user_input=input("\nHit x to quit,\n or input 'add' to Add Volunteer ")
        if user_input == "x":
            x=False
            #clear
        if user_input == "add":
            add_v = True
            while add_v:
                print("Enter quit to return to Menu")
            
                fname_loop = True
                while fname_loop:
                    fname = input("add first name: ")
                    if fname == "quit":
                        break
                    fname_valid=Validate.validate_name(fname) 
                    if fname_valid == None:
                        print("\n",Validate.name_error_message,"\n")
                    else:
                        fname_loop = False   
                if fname == "quit":
                    break      
            
                lname_loop = True
                while lname_loop:
                    lname = input("add last name: ")
                    if lname == "quit":
                        break
                    lname_valid=Validate.validate_name(lname)
                    if lname_valid == None:
                        print("\n",Validate.name_error_message,"\n")
                    else:
                       lname_loop = False   
                if lname == "quit":
                    break      

                email_loop = True          
                while email_loop:
                   email = input("add email: ")
                   if email == "quit":
                     email_loop = False
                     break
                   email_exist = session.query(Volunteer).filter(Volunteer.email == email).first()
                   if email_exist:
                       print("email already exist")
                   else:              
                       email_loop = False   
                if email == "quit":
                    break
   
                phone_loop = True  
                while phone_loop:
                    phone = input("add phone: ")
                    if phone == "quit":
                        break
                    phone_valid=Validate.validate_phone(phone) 
                    if phone_valid == None:
                        print("\n",Validate.phone_error_message,"\n")
                    else:
                        phone_loop = False   
                if phone == "quit":
                   break      
                
                floater_loop = True
                while floater_loop:
                    floater = input("floater? Y/N: ")
                    if floater == "quit":
                        break
                    floater_result = True if floater == 'Y' else False 
                    
                    floater_valid=Validate.validate_floater(floater_result)
                    if floater_valid == 'No':
                        print("\n",Validate.floater_error_message,"\n")
                    else:
                        floater_loop = False   
                if floater == "quit":
                    break      
           
                week_loop = True
                while week_loop:
                    week = input ("week [1-5]: ")
                    if week == "quit":
                        break
                    week_valid=Validate.validate_floater(week)
                    if week_valid == None:
                        print("\n",Validate.week_error_message,"\n")
                    else:
                        week_loop = False   
                if week == "quit":
                    break      
               
                position_loop = True
                while position_loop:
                    position = input ('Enter a  position [greeter, usher, welcome table, prayer]: ')
                    if position == "quit":
                        break
                    position_valid=Validate.validate_role(position)
                    if position_valid == None:
                        print("\n",Validate.role_error_message,"\n")
                    else:
                        position_loop = False   
                if position == "quit":
                    break      
            
                Volunteer.add_volunteer(fname, lname, email, phone, floater_result , week, position )

def delete_volunteer():
    pass

def modify_volunteer():
    pass

def add_to_schedule():
    pass

def modify_schedule():
    pass

def delete_schedule():
    pass

def print_schedule_by_name():
    pass

def print_schedule_by_date():
    pass

def swap_user():
    pass

def add_role():
    pass

def delete_role():
    pass

banner = '''
WELCOME TO The Scheduler
*****************************
'''
def start():
    while True:
        banner =  '''
        WELCOME TO The Scheduler
        *****************************
         '''
                
        print("Welcome to The Scheduler \n")
        print("1) Add Volunteer")
        print("2) Delete Volunteer")
        print("3) Modify Volunteer")
        print("4) Add Schedule")
        print("5) Modify Schedule")
        print("6) Delete Schedule")
        print("7) Print Shedule by Date")
        print("8) Print Schedule by Username")
        print("9) Volunteer Swap")
        print("10) Add Role")
        print("11) Delete Role")
        print("Q) Quit")
       
        user_input = input("What would you like to do? ")
        user_input = user_input.strip()

        if user_input == "1":
    
            add_volunteer()
        elif user_input == "2":
            delete_volunteer()
        elif user_input == "3":
            modify_volunteer()
        elif user_input == "4":
             add_to_schedule()
        elif user_input == "5":
            modify_schedule()
        elif user_input == "6":
            delete_schedule()
        elif user_input == "7": 
            print_schedule_by_date()
        elif user_input == "8":
            print_schedule_by_name()
        elif user_input == "9":
            swap_user()
        elif user_input == "10":
             add_role()
        elif user_input == "11":
             delete_role()  
        elif user_input == t:
            break


if __name__ == '__main__':
    start()
    
    