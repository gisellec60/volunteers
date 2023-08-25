#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import  Volunteer, Schedule, Validate
from simple_term_menu import TerminalMenu
from prettycli import red, green
from user_functions import (
    clear_screen, user_exist,
    keep_output_on_screen
)
from messages import(
    fname_input_message, lname_input_message, name_error_message,
    email_error_message, email_input_message, phone_error_message,
    phone_input_message, role_error_message, role_input_message, 
    floater_error_message, floater_input_message, week_error_message, 
    week_input_message 
)
engine = create_engine('sqlite:///volunteers.db')
Session = sessionmaker(bind=engine)
session = Session()

############################### Helper Functions #####################################################

# def user_exist(username):
#         volunteer = session.query(Volunteer).filter(Volunteer.username==username).first() 
#         return volunteer 

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
###################################################################################

def add_volunteer():
    print(red(add_banner))
    x=True
    complete = False
    while x:
        fname = get_volunteer_information("fname", fname_input_message, name_error_message)
        if fname == "X" or fname == "x":
           clear_screen()          
           x=False
           break 

        lname = get_volunteer_information("lname", lname_input_message, name_error_message)
        if lname == "X" or lname == "x":
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
 
        week = get_volunteer_information("week", week_input_message, week_error_message)
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
        print(green(f"\n{fname} {lname} <usrname: {volunteer.username}> successfully added to the Scheduler as a {role}"))
        keep_output_on_screen()
        clear_screen()

def delete_volunteer():
    print(red(delete_volunteer_banner))
    x=True
    while x:
        username = Validate.username_input()
        if username.upper() == "X":
           clear_screen()
           x=False
           break
        else:
            volunteer = user_exist(username)
            if volunteer:
                print(green(f'\n{volunteer.first_name} {volunteer.last_name} <username: {username}> was successfully deleted\n'))
                Volunteer.delete_volunteer(username)
                keep_output_on_screen()
                clear_screen()
                break
            else:
                username = input(red(f'\n{username} does not exist. Enter a valid username or x to quit '))    
                if username.upper() == "X":
                    clear_screen()
                    break

def modify_volunteer():
    print(red(modify_banner))
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
                loop = True
                while loop:
                    key_input = input("\nwhat would you like to change (Enter one) ? \n[first_name, last_name, email, phone,floater,week,role] ")
                    key_input = key_input.strip()
                    valid_key_input = Validate.validate_fields(key_input)

                    #because role is linked through a relational table it's handled differently
                    if valid_key_input:
                        if key_input == "role":
                            role_loop = True
                            while role_loop:
                                user_roles=[]
                                print("\n")
                                for role in volunteer.roles:
                                    print(role.position)
                                    user_roles.append(role.position)

                                #if volunteer has more than one role select role to change    
                                if(len(volunteer.roles)) > 1 :   
                                    input_role = input("\nEnter role to change: ")
                                    input_role = input_role.strip()
                                    if input_role not in user_roles:
                                        print(red(f"\n{input_role} is not one of the roles.\n"))
                                        user_continue = input("\nHit enter to continue or x to quit ")
                                        user_continue = user_continue.strip()
                                        if user_continue.upper() == "X" :
                                            x=False
                                            loop = False
                                            role_loop = False
                                            clear_screen()
                                            break
                                        else:
                                            continue 
                                #else just grab the one role
                                else: 
                                    for role in volunteer.roles:
                                        input_role = role.position

                                #Enter change for role    
                                value_input = input("\nEnter Change:  ")                    
                                value_input = value_input.strip()
                                roles_valid = Validate.validate_role(value_input)
                                if not roles_valid:
                                    print(red(f"\n{input_role} is not one of the roles.\n"))
                                    user_continue = input("\nHit enter to continue or x to quit ")
                                    user_continue = user_continue.strip()
                                    if user_continue.upper() == "X" :
                                        x=False
                                        role_loop=False
                                        loop = False
                                        clear_screen()
                                        break
                                    else:
                                        continue
                                else:
                                    changes["old"] = input_role
                                    changes[key_input] = value_input    
                                    role_loop = False
                                    break

                        else: # if key not = role
                            value_input = input("\nEnter Change: ")                    
                            value_input = value_input.strip()
                            changes[key_input] = value_input 
                        
                    else:  #if key_input not in input filed
                        print(red(f'\n{key_input} is not a valid field.\n'))
                        user_continue=input('\nHit enter if you want to continue or x to quit ')
                        if user_continue.upper() == "X":
                            loop = False
                            x=False
                            clear_screen()
                            break
                        else:
                             continue

                    user_continue = input("\nHit enter to make another change or x to continue  ") 
                    if user_continue.upper() == "X":
                        loop=False
                        break
                    else:
                        continue

                if len(changes) > 0:        
                    for key,value in changes.items():
                        if key.lower() == "floater":
                            new_value = True if value == 'Y' else False 
                            changes[key] = new_value
                        if key != 'old':    
                           print(f"\nchanging {key} to {value}...") 

                    Volunteer.modify_volunteer(username,changes)   
                    print(green("\nChange was sucessful"))
                    keep_output_on_screen()
                    clear_screen()
                    break

            else: #if username is valid
                print(red(f'{username} does not exist. Please check spelling.'))
                user_input= input("\nHit enter to continue or x to quit ")
                user_input = user_input.strip()
                if user_input.upper() == "X":
                    x=False
                    clear_screen()
                    break
                else:
                    continue

def add_to_schedule():
    print(red(add_schedule_banner))
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
                    role_input = input("\nEnter role: ")
                    role_input = role_input.strip()
                    role_valid = Validate.validate_role(role_input)
                    if role_valid: 
                        role_found = False
                        for role in volunteer.roles:
                            if role.position == role_input:
                                role_found = True
                        if role_found:
                            date_loop = True
                            while date_loop:
                                input_date = input("\nEnter date: YYY-MM-DD: ")
                                input_date = input_date.strip()
                                valid_date = Validate.validate_date(input_date) 
                                if not valid_date:
                                    print(red(f"\n{input_date} is an invalid date\n"))
                                    user_continue=input('Would you like to continue? Y/N ')
                                    if user_continue == "N" or user_continue == "n":
                                        sched_loop=False
                                        date_loop=False
                                        x=False
                                        clear_screen()
                                        break
                                    else:
                                        continue
                                else:
                                    date_loop=False
                                    break    
                            print("\nSchedule updating...")
                            Schedule.add_to_schedule(username, role_input, input_date)   
                            print(green(f"{username} added as a {role_input} to the schedule for {input_date}"))
                            keep_output_on_screen()
                            x=False
                            clear_screen()
                            break    
                        else:
                            print(red(f"\n{username} does not volunteer as a {role_input}")) 
                            user_input = input("\nWould you like to enter another role? Y/N ")  
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
    print(red(modify_schedule_banner))
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
                    print(red(f"{input_date} is not a valid date."))
                    user_continue = input("\nHit enter to for another date or x to quit  ")
                    if user_continue.upper() == "X":
                        date_loop = False
                        x = False
                        clear_screen()
                        break
                    else:
                        continue
                else:
                    #Is date in schedule for that volunteer?
                    valid_date = session.query(Schedule).filter(Schedule.date == input_date,
                                     Schedule.vol_id == volunteer.id).first()
                    if not valid_date:
                        print(red(f"{input_date} is not in the schedule"))
                        user_continue = input("\nHit enter to for another date or x to quit ")
                        if user_continue.upper() == "X":
                            date_loop = False
                            x = False
                            clear_screen()
                            break
                        else:
                            continue
                    else:    
                        date_input = input("\nHit enter to change the scheduled date or N to continue ")
                        date_input = date_input.strip()
                        if date_input.upper() == "N":
                            date_loop = False
                            break
                        else:
                            change_date = input("\nEnter valid date YYYY-MM-DD:")
                            change_date = change_date.strip()
                            valid_date = Validate.validate_date(change_date) 
                            if valid_date:
                                changes["date"]=change_date
                                date_loop = False
                            else:
                                print(red(f"{change_date} is not a valid date."))
                                user_continue = input("\nWould you like to enter another date Y/N? ")
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
    print(red(delete_schedule_banner))
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
                        schedule = session.query(Schedule).filter(Schedule.date == input_date, Schedule.vol_id == volunteer.id).first()
                        if schedule:
                            print("\n")
                            Schedule.delete_schedule(username,input_date)
                            print(green(f"\n{volunteer.first_name} {volunteer.last_name} has been successfully removed from the schedule for {input_date}\n"))
                            keep_output_on_screen()
                            date_loop = False
                            x = False
                            clear_screen()
                            break
                        else:
                            print(red(f"\nThere is no schedule for {volunteer.first_name} {volunteer.last_name} on {input_date}"))
                            user_continue = input("\nHit enter to re-enter date for x to quit ")
                            if user_continue.upper() == "X":
                                date_loop = False
                                x = False
                                clear_screen()
                                break
                            else:
                                continue  
                    else:
                        print(red(f"\n{input_date} is not a valid date."))
                        user_continue = input ("\nWould you like to enter another date Y/N? ")
                        if user_continue.upper() == "N":
                            date_loop = False
                            x = False
                            clear_screen()
                            break
                        else:
                            continue  

def print_schedule_by_name():
    print(red(query_by_name_banner))
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
                print(red(f"\n{username} does not exist."))
                user_continue = input ("\nWould you like to enter another username? Y/N ")    
                if user_continue.upper() == "N":
                    x=False
                    clear_screen()
                    break
                

def print_schedule_by_date():
    print(red(query_by_date_banner))
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
 
  _______ _             _____      _              _       _            
 |__   __| |           / ____|    | |            | |     | |           
    | |  | |__   ___  | (___   ___| |__   ___  __| |_   _| | ___ _ __  
    | |  | '_ \ / _ \  \___ \ / __| '_ \ / _ \/ _` | | | | |/ _ \ '__| 
    | |  | | | |  __/  ____) | (__| | | |  __/ (_| | |_| | |  __/ |    
    |_|  |_| |_|\___| |_____/ \___|_| |_|\___|\__,_|\__,_|_|\___|_|    
 
'''

add_banner = '''
=========================
    Add Volunteer
=========================
'''

delete_volunteer_banner = '''
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
delete_schedule_banner = '''
=============================
   Delete Schedule
=============================
'''

query_by_date_banner = '''
============================= 
   Query Schedule by Date
=============================
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
        else:
            print(red("You must select an option"))      


if __name__ == '__main__':
    main()
    
    