Changes I want to look into:

Two methods use this code.  Can I refactor it?

    schedule_date = datetime.strptime(input_date, '%Y-%m-%d').date()
        role = session.query(Role).filter(Role.position == role).first()
        volunteer=session.query(Volunteer).filter(Volunteer.username == username).one()
        schedule = session.query(Schedule).filter(Schedule.vol_id == volunteer.id,
               Schedule.date == schedule_date, Schedule.role_id == role.id).one() 

Make sure to add print statements for the methods.

Fix schedule dates so they are only on sundays.

CLI 
Validatons:

add_volunteer
   volunteer does not exist
   volunteer email is valid
   volunteer email is unique
   volunteer username unique  
   fname/lname are characters  !isdigit
   phone number are isdigit

delete_volunteer
   volunteer exist
modify_volunteer
    volunteer exist

Role:
Add role
   role is characters
Delete Role
   role exist   

Schedule:
  add_schedule:
    username exist
    role exist
    date is format "2023-08-30"
    date isdigit

  delete_schedule:
     username exist
     date correct format
     date isdigit

  modify_schedule:
     username exist
     date correct format
     date isdigit
     role is valid
     changes:
       name exist
       name !isdigit
       date is valid format and isdigit
       postion exist
  swap:
     usernanme exist 
     date is valid format and isdigit
     role exist
     swapname exist

  query_by_date
     date is valid format and isdigit

  query_by_name
     name exist      

Maker sure to strip all spaces from input:  user_input = user_input.strip()




  

