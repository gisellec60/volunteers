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
from prettycli import red, green

engine = create_engine('sqlite:///volunteers.db')
Session = sessionmaker(bind=engine)
session = Session()

############################### Functions #####################################################
role_error_message="role does not exist"
name_error_message="First and last name can only consist of A-z ,-,'."
email_error_message="Please enter a valid email"
phone_error_message="Please enter a valid phone number"
role_error_message="role does not exist"
user_exist_error_message="username does not exist"
floater_error_message="Floater value: Y or N"
week_error_message="Week must be an integer 1-5"
date_error_message=f"Please enter a valid date: YYY-MM-DD "

def week_input_message():
  return "\nEnter week [1-5] x to quit: "

role_input_message = "\nEnter a  position [greeter, usher, welcome table, prayer]: "



def validate_week(week):
    if week in [1,2,3,4,5]:
        return
    
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

def add_week():
    week_loop = True
    while week_loop:
        week = input ("\nEnter week of month to serve  [1-5]: ")
        if week.upper() == "X":
            break
        week_valid=Validate.validate_week(week)
        if not week_valid :
            print(red("\nWeek must be an integer 1-5\n"))
            week = input("\nHit Enter to try again or x to quit: ")
            if week.upper() == "X":
                week_loop = False
                break
            else:
                continue
        else:
            week_loop = False  
        return week   

def add_position():
    position_loop = True
    while position_loop:
        position = input ('\nEnter a  position [greeter, usher, welcome table, prayer]: ')
        if position.upper == "X":
            break
        else:
            position_valid=Validate.validate_role(position)
            if not position_valid :
                print(red(f"\n{position} is not a valid role!\n"))
                if position.upper() == "X":
                    position_loop = False
                    break
                else:
                    continue
            else:
                position_loop = False  
        return position   
    
def get_volunteer_information(field):
    loop = True
    while loop:
        field_input = input(f"{field}_input_message")
        if field_input.upper == "X":
            break
        else:
            field_valid = (f"validate_{field}(field_input)")
            if not field_valid :
                print(f"{field_input}_error_message,")
                field_input = input("\nHit enter to try again or x to quit: ")
                if field_input.upper() == "X":
                    loop = False
                    break
                else:
                    continue
            else:
                loop = False  
        return field_input   
###################################################################################

def add_volunteer():
    x=True
    while x:
        fname_loop = True
        while fname_loop:
            fname = input("\nEnter first name or x to quit: ")
            if fname.upper() == "X":
               break
            else:
                fname_valid=Validate.validate_name(fname) 
                if fname_valid:
                    fname_loop = False
                else:    
                    print(red("\nFirst and last name can only consist of A-z ,-,'.\n"))
                    fname = input("Enter to try again or x to quit ")
                    if fname.upper() == "X":
                         break
                    else:
                        continue   

        if fname.upper() == "X":
            clear_screen()
            x=False
            break 

        lname_loop = True
        while lname_loop:
            lname = input("\nEnter last name or x to quit:  ")
            if lname.upper() == "X":
                break
            else:
                lname_valid=Validate.validate_name(lname)
                if lname_valid:
                    lname_loop = False
                    break
                else:    
                    print(red("\nFirst and last name can only consist of A-z ,-,'.\n"))
                    lname = input("Hit enter to try again or x to quit ")
                    if lname.upper() == "X":
                        break
                    else:
                        continue  
   
        if lname.upper() == "X":
            clear_screen()
            x=False
            break 

        email_loop = True          
        while email_loop:
            email = input("\nEnter email or x to quit: ")
            if email.upper() == "X":
                break
            else:
                email_exist = session.query(Volunteer).filter(Volunteer.email == email).first()
                if email_exist:
                    print(red(f"\n{email} already exist\n"))
                    email = input("\nHit enter to try again or x to quit ")
                    if email.upper() == "X":
                       break
                    else:
                        continue
                else:
                    valid_email = Validate.validate_email(email)    
                    if valid_email:
                        email_loop = False
                        break
                    else:
                        email = input(red(f"\n{email} is invalid. Hit enter to try again or x to quit ")) 
                        if email.upper() == "X":
                               break
                        else:
                            continue
        
        if email.upper() == "X":
            clear_screen()
            x=False
            break 
   
        phone_loop = True  
        while phone_loop:
            phone = input("\nEnter phone number or x to quit: ")
            if phone.upper() == "X":
                phone_loop = False
                break
            phone_valid=Validate.validate_phone(phone) 
            if not phone_valid:
                print(red("\nPhone number is invalid\n"))
                phone = input(f"\nHit enter to try again or x to quit ")
                if email.upper() == "X":
                    phone_loop = False
                    break
                else:
                    continue
            else:
                phone_loop = False    

        if phone.upper() == "X":
            clear_screen()
            x=False
            break 
    
        floater_loop = True
        while floater_loop:
            floater_input = input("\nIs volunteer a floater? Y/N: ")
            if floater_input.upper() == "X":
                break
            if floater_input.upper( ) == "Y" or floater_input.upper() == "N":
                floater = True if floater_input == 'Y' else False 
                floater_loop = False
                break
            else:
                print(red("\nFloater value: Y or N\n"))
                floater_input = input(f"Hit enter to try again or x to quit ")
                if floater_input.upper() == "X":
                    floater_loop = False
                    break
                else:
                    continue

        if floater_input.upper() == "X":
           clear_screen()
           x=False
           break 
        
        week=add_week()
        # field = "week"
        # week = get_volunteer_information(field)
        if week.upper() == "X":
           x=False
           break 
 
        position = add_position()
        # field = "position"
        # position = get_volunteer_information(field)
        x=False
        break 

    volunteer = Volunteer.add_volunteer(fname, lname, email, phone, floater , week, position )
    print(green(f"\n{fname} {lname} <usrname: {volunteer.username}> successfully added to the schedule as a {position}"))
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
                print(f'\n{volunteer.first_name} {volunteer.last_name} {username} was successfully deleted\n')
                Volunteer.delete_volunteer(username)
                keep_output_on_screen()
                clear_screen() 
                break
            else:
                username = input(f'{username} does not exist. Enter a valid username or x to quit')    
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
                                        user_continue=input(f'\n{input_role} is not one of the roles.\nWould you like to continue? Y/N ')
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
                                    user_continue=input(f'\n{value_input} is not a valid role.\nWould you like to continue? Y/N ')
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
                        user_continue=input(f'\n{key_input} is not a valid field.\nWould you like to continue? Y/N ')
                        if user_continue == "N" or user_continue == "n":
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
                print("Change was sucessful")
                keep_output_on_screen()
                clear_screen() 
                break

            else: #if username is valid
                user_input = input(f'{username} does not exist. Please check spelling. Would you like to continue ?  Y/N  ')
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
                                print(Validate.date_error_message)
                                user_continue=input('Would you like to continue? Y/N ')
                                if user_continue == "N" or user_continue == "n":
                                    sched_loop=False
                                    x=False
                                    clear_screen()
                                    break
                            else:
                                print("\nSchedule updating...")
                                Schedule.add_to_schedule(username, role_input, input_date)   
                                print(f"Adding {username} as a {role_input} to the schedule for {input_date}")
                                keep_output_on_screen()
                                x=False
                                clear_screen()
                                break    
                        else:
                            user_input = input(f"{username} does not volunteer as a {role_input}. Would you like to enter another role? Y/N ")  
                            user_input = user_input.strip()
                            if user_input.upper() == "N":
                                x = False
                                sched_loop = False
                                clear_screen()
                                break
                            else:
                                continue
                    else:  
                        role_input = input(f"{role_input} is not a valid role. Would you like to continue ? Y/N ") 
                        role_input = role_input.strip()
                        if role_input.upper() == "N":
                            x=False
                            clear_screen()
                            break
                        else:
                            continue
            else: #if username is valid
                user_input = input(f'{username} does not exist. Please check spelling. Would you like to continue ?  Y/N  ')
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
                user_continue = input(f"{username} does not exit. Would you like to enter another username Y/N? ")
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
                           user_continue = input(f"{change_user} does not exist. Would you like to enter another username Y/N? ")
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
                    user_continue = input(f"{input_date} is not a valid date. Would you like to enter another date Y/N? ")
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
                            user_continue = input(f"{change_date} is not a valid date. Would you like to enter another date Y/N? ")
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
                    user_continue = input(f"{input_role} is not a valid role. Would you like to enter another role Y/N? ")
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
                            user_continue = input(f"\n{change_role} is not a valid role. Would you like to enter another role Y/N? ")
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
                user_continue = input(f"{username} does not exist. Would you like to enter another username Y/N? ")
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
                        print(f"\n{volunteer.first_name} {volunteer.last_name} has been removed from the schedule for {input_date}\n")
                        keep_output_on_screen()
                        date_loop = False
                        x = False
                        clear_screen()
                        break
                    else:
                        user_continue = input(f"\n{input_date} is not a valid date. Would you like to enter another date Y/N? ")
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
        # username = input("Enter username or x to exit: ")
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
                user_continue = input(f"{username} does not exist.  Would you like to enter another username? Y/N ")    
                if user_continue.upper() == "N":
                    x=False
                    clear_screen()
                    break
                

def print_schedule_by_date():
    # print(query_by_date_banner)
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
                user_continue = input("Invalid date. Would you like to re-enter the date Y/N ? ")
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

modify_schedule_banner = '''
    /   /    /     /    / 
   Modify Schedule
   /   /    /     /    /  
'''


def main():
    quitting = False
    while quitting == False:
        print(welcome_banner)
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


if __name__ == '__main__':
    main()
    
    