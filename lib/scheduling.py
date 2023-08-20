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
############################### Functions #####################################################
def user_exist(username):
        volunteer = session.query(Volunteer).filter(Volunteer.username==username).first() 
        return volunteer

def clear_screen():
        print("\n" * 40)

def user_exist(username):
        volunteer = session.query(Volunteer).filter(Volunteer.username==username).first() 
        return volunteer 

def keep_output_on_screen():
        user_input = input("x to exit: ") 
        user_input = user_input.strip()     
        return user_input


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
                    print("\n",Validate.name_error_message,"\n")
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
                else:    
                    print("\n",Validate.name_error_message,"\n")
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
            email = input("\nEnter last name or x to quit: ")
            if email.upper() == "X":
                break
            else:
                email_exist = session.query(Volunteer).filter(Volunteer.email == email).first()
                if email_exist:
                    print(f"{email} already exist")
                    email = input("Hit enter to try again or x to quit ")
                    if email.upper() == "X":
                       break
                    else:
                        continue
                else:
                    valid_email = Validate.validate_email(email)    
                    if valid_email:
                        email_loop = False
                    else:
                        email = input(f"{email} is invalid. Hit enter to try again or x to quit ") 
                        if email.upper() == "X":
                               break
                        else:
                            continue

        if email.upper() == "X":
            clear_screen()
            x=False
            break 
                 
   
   
    # phone_loop = True  
    # while phone_loop:
    #     phone = input("add phone: ")
    #     if phone == "quit":
    #         break
    #     phone_valid=Validate.validate_phone(phone) 
    #     if phone_valid == None:
    #         print("\n",Validate.phone_error_message,"\n")
    #     else:
    #         phone_loop = False   
    # if phone == "quit":
    #     break      
    
    # floater_loop = True
    # while floater_loop:
    #     floater = input("floater? Y/N: ")
    #     if floater == "quit":
    #         break
    #     floater_result = True if floater == 'Y' else False 
        
    #     floater_valid=Validate.validate_floater(floater_result)
    #     if floater_valid == 'No':
    #         print("\n",Validate.floater_error_message,"\n")
    #     else:
    #         floater_loop = False   
    # if floater == "quit":
    #     break      

    # week_loop = True
    # while week_loop:
    #     week = input ("week [1-5]: ")
    #     if week == "quit":
    #         break
    #     week_valid=Validate.validate_floater(week)
    #     if week_valid == None:
    #         print("\n",Validate.week_error_message,"\n")
    #     else:
    #         week_loop = False   
    # if week == "quit":
    #     break      
    
    # position_loop = True
    # while position_loop:
    #     position = input ('Enter a  position [greeter, usher, welcome table, prayer]: ')
    #     if position == "quit":
    #         break
    #     position_valid=Validate.validate_role(position)
    #     if position_valid == None:
    #         print("\n",Validate.role_error_message,"\n")
    #     else:
    #         position_loop = False   
    # if position == "quit":
    #     break      

    # volunteer = Volunteer.add_volunteer(fname, lname, email, phone, floater_result , week, position )
    # print(f"{fname} {lname} <usrname: {volunteer.username}> added to the schedule as a {position}")
    # user_input = keep_output_on_screen()
    # if user_input.upper() == "X":
    #     x=False
    #     clear_screen() 
    #     break

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
            exist_user = user_exist(username)
            if exist_user:
                volunteer = Volunteer.delete_volunteer(username)
                print(f'\n{volunteer.first_name} {volunteer.last_name} {username} was successfully deleted\n')
                # user_input = input("X to exit: ")  
                user_input = keep_output_on_screen()
                if user_input.upper() == "X":
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
                user_input = keep_output_on_screen()
                if user_input.lower() == "x" :
                    x=True
                    clear_screen() 
                    break
                else:
                    x=True
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
                                user_input = keep_output_on_screen()
                                if user_input.lower() == "x" :
                                    sched_loop=False
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
        user_input = keep_output_on_screen()
        if user_input.lower() == "x" :
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
                        user_input = keep_output_on_screen()
                        if user_input.upper() == "X" :
                           clear_screen()
                           date_loop=True
                           x = False
                           break
                        else:
                            clear_screen()
                            date_loop=True
                            x = False
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
                user_input = keep_output_on_screen()
                if user_input.lower() == "x" :
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
                # user_input = input("x to exit: ") 
                # user_input = user_input.strip() 
                user_input = keep_output_on_screen()
                if user_input.lower() == "x" :
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
    
    