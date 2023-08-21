#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from model import  Volunteer, Role, Schedule, Validate
import re
from datetime import datetime, date
from simple_term_menu import TerminalMenu
from prettycli import red, green, blue

engine = create_engine('sqlite:///volunteers.db')
Session = sessionmaker(bind=engine)
session = Session()

############################### Helper Functions #####################################################


fname_input_message="\nEnter first name or x to quit: "
lname_input_message="\nEnter last name or x to quit: "
name_error_message="First and last name can only consist of A-z ,-,'."

email_error_message="Please enter a valid email"
email_input_message="\nEnter email or x to quit "

phone_error_message="Please enter a valid phone number"
phone_input_message="\nEnter phone number or x to quit: "

role_error_message="role does not exist"
role_input_message = "\nEnter a  position [greeter, usher, welcome table, prayer]: "

user_exist_error_message="username does not exist"

floater_error_message="Floater value: Y or N"
floater_input_message ="\nIs volunteer a floater? Y/N or x to quit: "

week_error_message="Week must be an integer 1-5"
week_input_message="\nEnter week [1-5] x to quit: "

date_error_message=f"Please enter a valid date: YYY-MM-DD "

def validate(field, field_input):
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
        print("are you getting here")
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

def user_exist(username):
        volunteer = session.query(Volunteer).filter(Volunteer.username==username).first() 
        return volunteer

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


def get_volunteer_information(field, input_message, error_message):
    loop = True
    while loop:
        field_input = input(input_message)
        if field_input == "X" or field_input == "x":
            break
        else:
            field_valid = validate(field, field_input)
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
###################################################################################

def add_volunteer():
    x=True
    complete = False
    while x:
        fname = get_volunteer_information("fname", fname_input_message, name_error_message)
        if fname == "X" or fname == "x":
           clear_screen()
           x=False
           break 

        lname = get_volunteer_information("lname", lname_input_message, name_error_message)
        if lname == "X" or fname == "x":
           clear_screen()
           x=False
           break 

        email = get_volunteer_information("email", email_input_message, email_error_message)
        if email == "X" or email == "x":
           clear_screen()
           x=False
           break 

        phone = get_volunteer_information("phone", phone_input_message, phone_error_message)
        if phone == "X" or phone == "x":
           clear_screen()
           x=False
           break 

        floater = get_volunteer_information("floater", floater_input_message, floater_error_message)
        if floater == "X"or floater == "x":
           clear_screen()
           x=False
           break 
 
        week = get_volunteer_information("week", week_input_message,week_error_message)
        print(week)
        if week == "X" or week == "x":
           x=False
           clear_screen()
           break 
 
        role = get_volunteer_information("role", role_input_message, role_error_message)
        if role:
           complete = True 
        x=False
        break 

    if complete: 
        volunteer = Volunteer.add_volunteer(fname, lname, email, phone, floater , week, role )
        print(green(f"\n{fname} {lname} <usrname: {volunteer.username}> successfully added to the schedule as a {role}"))
        keep_output_on_screen()
        clear_screen() 
       

def delete_volunteer():
    print(delete_banner)
    x=True
    while x:
        username = Validate.username_input()
        if username.upper() == "X":
           clear_screen() 
           x=False
           break
        else:
            # user_exist = session.query(Volunteer).filter(Volunteer.username == username).first()
            volunteer = user_exist(username)
            if volunteer:
                print(green(f'\n{volunteer.first_name} {volunteer.last_name} {username} was successfully deleted\n'))
                Volunteer.delete_volunteer(username)
                keep_output_on_screen()
                clear_screen() 
                break
            else:
                username = input(red(f'{username} does not exist. Enter a valid username or x to quit'))    
                if username.upper() == "X":
                    clear_screen()
                    break

def modify_volunteer():
    clear_screen() 
    print(modify_banner)
    x=True
    changes={}
    while x:
        username = input("Enter username or X to quit: ")
        if username.upper() == "X":
           clear_screen() 
           break
        else:
            volunteer = user_exist(username)
            if volunteer:
                change_loop = True
                while change_loop:
                    key_input = input("\nwhat would you like to change (Enter one) ? \n[first_name, last_name, email, phone,floater,week,role] ")
                    key_input = key_input.strip()
                    valid_key_input = Validate.validate_fields
                    
                    #because role is linked through a relational table it's handled differently
                    if valid_key_input:
                        if key_input == "role":
                            role_loop = True
                            while role_loop:
                                if(len(volunteer.roles)) > 1 :
                                    print("\n")
                                    user_roles=[]
                                    for role in volunteer.roles:
                                        print(role.position)
                                        user_roles.append(role.position)
                                    input_role = input("\nEnter role to change: ")
                                    input_role = input_role.strip()
                                    roles_valid = Validate.validate_role(input_role)
                                    if not roles_valid:
                                        user_continue=input(red(f'\n{input_role} is not one of the roles.\nWould you like to continue? Y/N '))
                                        user_continue = user_continue.strip()
                                        if user_continue.upper() == "N" :
                                            x=False
                                            change_loop = False
                                            role_loop = False
                                            clear_screen()
                                            break
                                        else:
                                            continue  
                                else: #if volunteer.roles = 1 
                                    for role in volunteer.roles:
                                        input_role = role.position

                                value_input = input("Enter Change:  ")                    
                                value_input = value_input.strip()
                                roles_valid = Validate.validate_role(input_role)
                                if not roles_valid:
                                    user_continue=input(red(f'\n{value_input} is not a valid role.\nWould you like to continue? Y/N '))
                                    if user_continue.upper() == "N" :
                                        x=False
                                        role_loop=False
                                        change_loop = False
                                        clear_screen()
                                        break
                                    else:
                                        continue
                                else:    
                                    changes[key_input] = value_input
                                    changes["old"] = input_role
                                    role_loop = False

                        else: # if key not = role
                            value_input = input("Enter Change:  ")                    
                            value_input = value_input.strip()
                            changes[key_input] = value_input 

                        user_continue = input("\nMaking another change? Y/N ") 
                        if user_continue.upper() == "N":
                            change_loop = False
                            break
                        else:
                            continue

                    else:  #if key_input not in input filed
                        user_continue=input(red(f'\n{key_input} is not a valid field.\nWould you like to continue? Y/N '))
                        if user_continue.upper() == "N":
                            change_loop = False
                            x=False
                            clear_screen()
                            break
                        else:
                             continue
                        
                for key,value in changes.items():
                    if key.lower() == "floater":
                        new_value = True if value == 'Y' else False 
                        changes[key] = new_value
                    if key != 'old':    
                       print(f"\nchanging {key} to {value}...") 

                Volunteer.modify_volunteer(username,changes)   
                print(green("Change was sucessful"))
                keep_output_on_screen()
                clear_screen() 
                break

            else: #if username is valid
                user_input = input(red(f'{username} does not exist. Please check spelling. Would you like to continue ?  Y/N  '))
                user_input = user_input.strip()
                if user_input.upper() == "N":
                    change_loop = False
                    x=False
                    clear_screen()
                    break
                else:
                    continue

def add_to_schedule():
    clear_screen() 
    print(add_schedule_banner)
    x=True
    sched_loop = False
    while x:
        username = input("Enter username or X to quit: ")
        if username.upper() == "X":
           clear_screen() 
           break
        else:
            volunteer = user_exist(username)
            if volunteer:
                sched_loop = True
                while sched_loop:
                    role_input = input("Enter role: ")
                    role_input = role_input.strip()
                    role_valid = Validate.validate_role(role_input)
                    if role_valid: 
                        role_found = False
                        for role in volunteer.roles:
                            if role.position == role_input:
                                role_found = True
                        if role_found:
                            input_date = input("Enter date: YYY-MM-DD: ")
                            input_date = input_date.strip()
                            valid_date = Validate.validate_date(input_date) 
                            if valid_date == None:
                                print(red(f"\n{input_date} is an invalid date\n"))
                                user_continue=input('Would you like to continue? Y/N ')
                                if user_continue == "N" or user_continue == "n":
                                    sched_loop=False
                                    x=False
                                    clear_screen()
                                    break
                            else:
                                print("\nSchedule updating...")
                                Schedule.add_to_schedule(username, role_input, input_date)   
                                print(green(f"{username} added as a {role_input} to the schedule for {input_date}"))
                                keep_output_on_screen()
                                x=False
                                clear_screen()
                                break    
                        else:
                            user_input = input(red(f"{username} does not volunteer as a {role_input}. Would you like to enter another role? Y/N "))  
                            user_input = user_input.strip()
                            if user_input.upper() == "N":
                                x = False
                                sched_loop = False
                                clear_screen()
                                break
                            else:
                                continue
                    else:  
                        role_input = input(red(f"{role_input} is not a valid role. Would you like to continue ? Y/N ")) 
                        role_input = role_input.strip()
                        if role_input.upper() == "N":
                            x=False
                            clear_screen()
                            break
                        else:
                            continue
            else: #if username is valid
                user_input = input(red(f'{username} does not exist. Please check spelling. Would you like to continue ?  Y/N  '))
                user_input = user_input.strip()
                if user_input.upper() == "N":
                    x=False
                    clear_screen()
                    break

def modify_schedule():
    print(modify_schedule_banner)
    changes = {}
    user_loop = True
    x=True
    while x:
        username = input("Enter usersname for current schedule or x to quit: ")
        username = username.strip()
        if username.upper() == "X":
           x=False
           clear_screen() 
           break
        else:
            volunteer = user_exist(username)
            if not volunteer:
                user_continue = input(red(f"{username} does not exit. Would you like to enter another username Y/N? "))
                if user_continue.upper() == "N":
                    x=False
                    clear_screen()
                    break
                else:
                    continue
            else:
                while user_loop:
                    user_input = input("\nWould you like to change the scheduled volunteer Y/N ? ")
                    user_input = user_input.strip()
                    if user_input.upper() == "N":
                        user_loop = False
                    else:
                        change_user = input("Enter username: ")
                        change_user = change_user.strip()
                        valid_user = user_exist(change_user)
                        if valid_user:
                            changes["username"]=change_user
                            user_loop = False
                        else:
                           user_continue = input(red(f"{change_user} does not exist. Would you like to enter another username Y/N? "))
                           if user_continue.upper() == "N":
                                user_quit = input("Would like to continue Y/N? ")
                                if user_quit.upper() == "N":
                                    user_loop = False
                                    x = False
                                    clear_screen()
                                    break
                                else:
                                    user_loop = False
                           else:
                               continue    

            date_loop = True
            while date_loop:
                input_date = input("\nEnter scheduled date YYYY-MM-DD: ")
                input_date = input_date.strip()
                valid_date = Validate.validate_date(input_date) 
                if not valid_date:
                    user_continue = input(red(f"{input_date} is not a valid date. Would you like to enter another date Y/N? "))
                    if user_continue.upper() == "N":
                        date_loop = True
                        clear_screen()
                        break
                else:
                    date_input = input("Would you like to change the scheduled date Y/N? ")
                    date_input = date_input.strip()
                    if date_input.upper() == "N":
                         date_loop = False
                    else:
                        change_date = input("\nEnter valid date YYYY-MM-DD:")
                        change_date = change_date.strip()
                        valid_date = Validate.validate_date(change_date) 
                        if valid_date:
                            changes["date"]=change_date
                            date_loop = False
                        else:
                            user_continue = input(red(f"{change_date} is not a valid date. Would you like to enter another date Y/N? "))
                            if user_continue.upper() == "N":
                                user_quit = input("Would like to continue Y/N? ")
                                if user_quit.upper() == "N":
                                    date_loop = False
                                    clear_screen()
                                    break
                                else:
                                    continue
                
            role_loop = True
            while role_loop:
                input_role = input("\nEnter the scheduled role: ") 
                input_role = input_role.strip()
                valid_role = Validate.validate_role(input_role)
                if not valid_role:
                    user_continue = input(red(f"{input_role} is not a valid role. Would you like to enter another role Y/N? "))
                    if user_continue.upper() == "N":
                        role_loop = False
                        clear_screen()
                        break
                    else:
                        continue
                else:
                    role_input = input("\nWould you like to change the scheduled role Y/N ?")
                    role_input = role_input.strip()
                    if role_input.upper() == "N":
                        role_loop = False
                    else:
                        change_role = input("\nEnter a valid role: ")    
                        change_role = change_role.strip()  
                        valid_change_role = Validate.validate_role(change_role)
                        if valid_change_role:
                            changes['role'] = change_role
                            role_loop = False
                            break
                        else:  
                            user_continue = input(red(f"\n{change_role} is not a valid role. Would you like to enter another role Y/N? "))
                            if user_continue.upper() == "N":
                                user_quit = input("Would like to continue Y/N? ")
                                if user_quit.upper() == "N":
                                    date_loop = False
                                    clear_screen()
                                    break
                                else:
                                    continue
                                          
        Schedule.modify_schedule(username, input_date, input_role,changes) 
        keep_output_on_screen()
        clear_screen()
        break

def delete_schedule():
    x=True
    while x:
        username=Validate.username_input()
        if username.upper() == "X" :
           clear_screen()
           x=False
        else:   
            volunteer = user_exist(username)
            if not volunteer:
                user_continue = input(red(f"{username} does not exist. Would you like to enter another username Y/N? "))
                if user_continue.upper() == "N":
                    x=False
                    clear_screen()
                    break
                else:
                    continue
            else:
                date_loop = True
                while date_loop:
                    input_date = input("\nEnter valid date YYYY-MM-DD: ")
                    valid_date = Validate.validate_date(input_date) 
                    if valid_date:
                        print("\n")
                        Schedule.delete_schedule(username,input_date)
                        print(green(f"\n{volunteer.first_name} {volunteer.last_name} has been successfully removed from the schedule for {input_date}\n"))
                        keep_output_on_screen()
                        date_loop = False
                        x = False
                        clear_screen()
                        break
                    else:
                        user_continue = input(red(f"\n{input_date} is not a valid date. Would you like to enter another date Y/N? "))
                        if user_continue.upper() == "N":
                            date_loop = False
                            x = False
                            clear_screen()
                            break
                        else:
                            continue  

def print_schedule_by_name():
    print(query_by_name_banner)
    x=True
    while x:
        username=Validate.username_input()
        if username.upper() == "X":
           clear_screen() 
           x=False
           break
        else:
            volunteer = session.query(Volunteer).filter(Volunteer.username==username).first() 
            if volunteer:
                Schedule.query_by_name(username)
                print("\n")
                keep_output_on_screen()
                clear_screen()
                break    
            else:
                user_continue = input(red(f"{username} does not exist.  Would you like to enter another username? Y/N "))    
                if user_continue.upper() == "N":
                    x=False
                    clear_screen()
                    break
                

def print_schedule_by_date():
    #print(query_by_date_banner)
    x=True
    while x:
        date_input = input("Enter x to quit or a valid date YYY-MM-DD: ")
        if date_input.upper() == "X":
           clear_screen() 
           x=False
           break 
        else:
            valid_date = Validate.validate_date(date_input)
            if valid_date:
                Schedule.query_by_date(date_input)
                keep_output_on_screen()
                clear_screen()
                break    
            else:
                user_continue = input(red("Invalid date. Would you like to re-enter the date Y/N ? "))
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
=========================
    Delete Volunteer
=========================
'''

modify_banner = '''
===========================
     Modify Volunteer
===========================
'''
add_schedule_banner = '''
============================
     Add Schedule
============================
'''

query_by_name_banner = '''
============================ 
   Query Schedule by Name
============================
'''

modify_schedule_banner = '''
=============================
   Modify Schedule
=============================
'''
query_by_date_banner = '''
============================= 
   Query Schedule by Name
=============================
'''

def main():
    quitting = False
    while quitting == False:
        print(blue(welcome_banner))
        options = ["Add Volunteer", "Delete Volunteer", "Modify Volunteer", "Add Schedule", "Modify Schedule", "Delete Schedule","Print Schedule by Date","Print Schedule by Name","Quit"]
        terminal_menu = TerminalMenu(options)
        options_index = terminal_menu.show()
        options_choice = options[options_index]
   
        if options_choice == "Add Volunteer": 
            add_volunteer()
        elif options_choice == "Delete Volunteer":
             delete_volunteer()  
        elif options_choice == "Modify Volunteer":
             modify_volunteer()
        elif options_choice == "Add Schedule":
             add_to_schedule()
        elif options_choice == "Modify Schedule":
            modify_schedule()
        elif options_choice == "Delete Schedule":
            delete_schedule()
        elif options_choice == "Print Schedule by Date":
            print_schedule_by_date()
        elif options_choice == "Print Schedule by Name":
            print_schedule_by_name() 
        elif options_choice == "Quit":
            clear_screen()
            quitting = True  
        else:
            print(red("You must select an option"))      


if __name__ == '__main__':
    main()
    
    