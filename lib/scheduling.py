#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from model import  Volunteer, Role, Schedule, Validate
import click
import ipdb
from datetime import datetime, date
from simple_term_menu import TerminalMenu
from prettycli import red, yellow

engine = create_engine('sqlite:///volunteers.db')
Session = sessionmaker(bind=engine)
session = Session()

def user_exist(username):
        volunteer = session.query(Volunteer).filter(Volunteer.username==username).first() 
        return volunteer

def clear_screen():
        print("\n" * 40)
ans=["Y","N"]
def add_volunteer():
    x=True
    add_v = False
    print(welcome_banner)
    while x:
        print ("Add Volunteer")
        user_input=input("\nHit x to quit,\n or input 'add' to Add Volunteer ")
        if user_input == "x" or user_input == "X":
            x=False
            clear_screen()

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
    print(delete_banner)
    x=True
    while x:
        username = input("Enter username or X to quit: ")
        if username == "x" or username == "X":
           clear_screen() 
           break
        else:
            user_exist = session.query(Volunteer).filter(Volunteer.username == username).first()
        if  user_exist:
            Volunteer.delete_volunteer(username)
            print(f'\n{username} was successfully deleted\n')
            user_input = input("X to exit: ")  
            if user_input == "x" or user_input == "X":
                clear_screen() 
                break
        else:
            username = input(f'{username} does not exist. Enter a valid username or x to quit')    
            if username == "x" or username == "X":
                clear_screen()
                break

def modify_volunteer():
    clear_screen() 
    print(modify_banner)
    valid_fields = ["first_name", "last_name", "email", "phone","floater","week","role"]
    valid_roles = ["greeter", "usher","welcome table","prayer"]
    x=True
    changes={}
    ans=["Y","N"]
    while x:
        username = input("Enter username or X to quit: ")
        if username.upper() == "X":
           clear_screen() 
           break
        else:
            user_exist = session.query(Volunteer).filter(Volunteer.username == username).first()  
           
            if user_exist:
                dic_loop = True
                while dic_loop:

                    key_input = input("\nwhat would you like to change (Enter one) ? \n[first_name, last_name, email, phone,floater,week,role] ")
                    key_input = key_input.strip()
                    
                    if key_input in valid_fields:
                        if key_input == "role":
                            volunteer = session.query(Volunteer).filter(Volunteer.username == username).first()
                            if (len(volunteer.roles)) > 1 :
                                print("\n")
                                user_roles=[]
                                for role in volunteer.roles:
                                    print(role.position)
                                    user_roles.append(role.position)
                                role_loop = True
                                while role_loop:
                                    input_role = input("\nEnter role to change: ")
                                    input_role = input_role.strip()
                                    if input_role not in user_roles:
                                       user_continue=input(f'\n{input_role} is not one of the roles.\nWould you like to continue? Y/N ')
                                       user_continue = user_continue.strip()
                                       if user_continue.upper() in ans:
                                           if user_continue.upper() == "N" :
                                                x=False
                                                dic_loop = False
                                                clear_screen()
                                                break
                                    else:
                                        break  
                            else: #if volunteer.roles = 1 
                                for role in volunteer.roles:
                                    input_role = role.position
                            role_loop = True
                            while role_loop:
                                value_input = input("Enter Change:  ")                    
                                value_input = value_input.strip()
                                if value_input not in valid_roles:
                                    user_continue=input(f'\n{value_input} is not a valid role.\nWould you like to continue? Y/N ')
                                    if user_continue.upper() in ans:
                                        if user_continue.upper() == "N" :
                                            x=False
                                            dic_loop=False
                                            clear_screen()
                                            break
                                else:
                                    changes[key_input] = value_input
                                    changes["old"] = input_role
                                    role_loop = False
                        else: # if key not = role
                            value_input = input("Enter Change:  ")                    
                            value_input = value_input.strip()
                            changes[key_input] = value_input 
                        user_continue = input("\nMaking another change? Y/N ") 
                        if user_continue.upper() in ans:
                            if user_continue.upper() == "N":
                                print ("do you get here")
                                x=False
                                clear_screen()
                                break
                    else:  #if key_input not in input filed
                        user_continue=input(f'\n{key_input} is not a valid field.\nWould you like to continue? Y/N ')
                        if user_continue.upper() in ans:
                            if user_continue == "N" or user_continue == "n":
                                x=False
                                clear_screen()
                                break
          
            for key,value in changes.items():
                if key.lower() == "floater":
                    new_value = True if value == 'Y' else False 
                    changes[key]=new_value
                print(f"\nchanging {key} to {value}...")  
                Volunteer.modify_volunteer(username,changes)   
                print("Change was sucessful")
                user_input = input("x to exit: ") 
                user_input = user_input.strip() 
                if user_input.lower() == "x" :
                    clear_screen() 
                    break

            else: #if username is valid
                user_input = input(f'{username} does not exist. Please check spelling. Would you like to continue ?  Y/N  ')
                user_input = user_input.strip()
                if user_input.upper() in ans:
                    if user_input.upper() == "N":
                        x=False
                        clear_screen()
                        break

def add_to_schedule():
    clear_screen() 
    print(add_schedule_banner)
    ans=["Y","N"]
    valid_roles = ["greeter", "usher","welcome table","prayer"]
    x=True
    sched_loop = False
    user_roles=[]
    while x:
        username = input("Enter username or X to quit: ")
        if username.upper() == "X":
           clear_screen() 
           break
        else:
            user_exist = session.query(Volunteer).filter(Volunteer.username == username).first()
            if user_exist:
                sched_loop = True
                while sched_loop:
                    role_input = input("Enter role: ")
                    role_input = role_input.strip()
                    if role_input in valid_roles:
                        volunteer = session.query(Volunteer).filter(Volunteer.username == username).first()
                        for role in volunteer.roles:
                            user_roles.append(role.position)
                        if role_input in user_roles:  
                            input_date = input("Enter date: YYY-MM-DD: ")
                            input_date = input_date.strip()
                            valid_date = Validate.validate_date(input_date) 
                            if valid_date == None:
                                print(Validate.date_error_message)
                                user_continue=input('Would you like to continue? Y/N ')
                                if user_continue.upper() in ans:
                                    if user_continue == "N" or user_continue == "n":
                                        sched_loop=False
                                        x=False
                                        clear_screen()
                                        break
                            else:
                                print("\nSchedule updating...")
                                Schedule.add_to_schedule(username, role_input, input_date)   
                                print(f"Adding {username} as a {role_input} to the schedule for {input_date}")
                                user_input = input("x to exit: ") 
                                user_input = user_input.strip() 
                                if user_input.lower() == "x" :
                                    sched_loop=False
                                    x=False
                                    clear_screen()
                                    break    
                        else:
                            user_input = input(f"{username} does not volunteer as a {role_input}. Would you like to enter another role? Y/N ")  
                            user_input = user_input.strip()
                            if user_input.upper() in ans:
                                if user_input.upper() == "N":
                                    x=False
                                    clear_screen()
                                    break
                                else:
                                    break
                    else:  
                        role_input = input(f"{role_input} is not a valid role. Would you like to continue ? Y/N ") 
                        role_input = role_input.strip()
                        if role_input.upper() in ans:
                            if role_input.upper() == "N":
                                x=False
                                clear_screen()
                                break
                            else:
                                break
                        
            else: #if username is valid
                user_input = input(f'{username} does not exist. Please check spelling. Would you like to continue ?  Y/N  ')
                user_input = user_input.strip()
                if user_input.upper() in ans:
                    if user_input.upper() == "N":
                        x=False
                        clear_screen()
                        break

def modify_schedule():
    changes = {}
    x=True
    while x:

        user_loop = True
        while user_loop:
            username = input("Enter usersname for current schedule or x to quit: ")
            username = username.strip()
            volunteer = user_exist(username)
            if not volunteer:
                user_continue = input(f"{username} does not exit. Would you like to enter another username Y/N? ")
                if user_continue.upper() in ans:
                    if user_continue.upper() == "N":
                        x=False
                        clear_screen()
                        break
            else:
                user_input = input("Would you like to change this volunteer Y/N ? ")
                user_input = user_input.strip()
                if user_input.upper() in ans:
                    if user_input.upper() == "N":
                        break

                    else:
                        change_user = input("Enter username: ")
                        change_user = change_user.strip()
                        valid_user = user_exist(change_user)
                        if valid_user:
                            changes["username"]=valid_user
                        else:
                            user_continue = input(f"{valid_user} does not exit. Would you like to enter another username Y/N? ")
                            if user_continue.upper() in ans:
                                if user_continue.upper() == "N":
                                    user_quit = input("Would like to continue Y/N? ")
                                    if user_quit.upper() == "N":
                                        user_loop = False
                                        x = False
                                        clear_screen()
                                        break
                                    else:
                                        user_loop = False

            date_loop = True
            while date_loop:
                input_date = input("Enter valid date YYYY-MM-DD: ")
                input_date = input_date.strip()
                valid_date = Validate.validate_date(input_date) 
                if not valid_date:
                    user_continue = input(f"{input_date} is not a valid date. Would you like to enter another date Y/N? ")
                    if user_continue.upper() in ans:
                        if user_continue.upper() == "N":
                            date_loop = True
                            x=False
                            clear_screen()
                            break
                else:
                    date_input = input("Would you like to change the date Y/N? ")
                    date_input = date_input.strip()
                    if date_input.upper() in ans:
                        if date_input.upper() == "N":
                           break
                    else:
                        change_date = input("Enter valid date YYYY-MM-DD:")
                        change_date = change_date.strip()
                        valid_date = Validate.validate_date(change_date) 
                        if valid_date:
                           changes["date"]=valid_date
                        else:
                           user_continue = input(f"{change_date} is not a valid date. Would you like to enter another date Y/N? ")
                           if user_continue.upper() in ans:
                              if user_continue.upper() == "N":
                                    user_quit = input("Would like to continue Y/N? ")
                                    if user_quit.upper() == "N":
                                        date_loop = False
                                        x = False
                                        clear_screen()
                                        break
                                    else:
                                        date_loop = False
                 
            role_loop = True
            while role_loop:
                input_role = input("Enter valid role: ") 
                input_role = input_role.strip()
                valid_role = Validate.validate_role(input_role)
                if not valid_role:
                    user_continue = input(f"{input_role} is not a valid role. Would you like to enter another role Y/N? ")
                    if user_continue.upper() in ans:
                        if user_continue.upper() == "N":
                            x=False
                            clear_screen()
                            break
                else:
                   role_input = input("Would you like to change the role Y/N ?")
                   role_input = role_input.strip()
                   if role_input.upper() in ans:
                      if role_input.upper() == "N":
                         break
                      else:
                          change_role = input("Enter a valid role: ")    
                          change_role = change_role.strip()  
                          valid_change_role = Validate.validate_role(change_role)
                          if valid_change_role:
                              changes['role'] = change_role
                          else:  
                              user_continue = input(f"{change_role} is not a valid role. Would you like to enter another role Y/N? ")
                              if user_continue.upper() in ans:
                                  if user_continue.upper() == "N":
                                      user_quit = input("Would like to continue Y/N? ")
                                      if user_quit.upper() == "N":
                                           date_loop = False
                                           x = False
                                           clear_screen()
                                           break
                                      else:
                                           date_loop = False
        print(changes) 
        print(username, input_date, input_role)                                  
        # Schedule.modify_schedule(username, input_date, input_role,changes) 


def delete_schedule():
    pass

def print_schedule_by_name():
    print(query_by_name_banner)
    x=True
    while x:
        username = input("Enter username or x to exit: ")
        if username.upper() == "X":
           clear_screen() 
           break
        volunteer = session.query(Volunteer).filter(Volunteer.username==username).first() 
        if volunteer:
            Schedule.query_by_name(username)
            user_input = input("x to exit: ") 
            user_input = user_input.strip() 
            if user_input.lower() == "x" :
                clear_screen()
                break    
        else:
            user_continue = input(f"{username} does not exist.  Would you like to enter another username? Y/N ")    
            if user_continue.upper() in ans:
                if user_continue.upper() == "N":
                    x=False
                    clear_screen()
                    break
                

def print_schedule_by_date():
    print(query_by_name_banner)
    x=True
    while x:
        date_input = input("Enter a valid date YYY-MM-DD: ")
        valid_date = Validate.validate_date(date_input)
        if valid_date:
            Schedule.query_by_date(date_input)
            user_input = input("x to exit: ") 
            user_input = user_input.strip() 
            if user_input.lower() == "x" :
                clear_screen()
                break    
        else:
            user_continue = input("Invalid date. Would you like to re-enter the date Y/N ? ")
            if user_continue.upper() in ans:
                if user_continue.upper() == "N":
                    x=False
                    clear_screen()
                    break


def swap_user():
    pass

def add_role():
    pass

def delete_role():
    pass

welcome_banner = '''
  WELCOME TO The Scheduler
*****************************
'''
delete_banner = '''
   /   /    /     /    / 
    Delete Volunteer
  /   /    /     /    /  
'''

modify_banner = '''
    /   /    /     /    / 
     Modify Volunteer
   /   /    /     /    /  
'''
add_schedule_banner = '''
    /   /    /     /    / 
     Add Schedule
   /   /    /     /    /  
'''

query_by_name_banner = '''
    /   /    /     /    / 
   Query Schedule by Name
   /   /    /     /    /  
'''

def start():
    while True:
        print(welcome_banner)
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
       
        user_input = input("\nWhat would you like to do? ")
        user_input = user_input.strip()

        if user_input == "1":
            clear_screen() 
            add_volunteer()
        elif user_input == "2":
            clear_screen()
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
            clear_screen()
            print_schedule_by_name()
        elif user_input == "9":
            swap_user()
        elif user_input == "10":
             add_role()
        elif user_input == "11":
             delete_role()  
        elif user_input == "q" or user_input == "Q":
            break


if __name__ == '__main__':
    start()
    
    