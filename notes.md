Changes I want to look into:

Two methods use this code.  Can I refactor it?

    schedule_date = datetime.strptime(input_date, '%Y-%m-%d').date()
        role = session.query(Role).filter(Role.position == role).first()
        volunteer=session.query(Volunteer).filter(Volunteer.username == username).one()
        schedule = session.query(Schedule).filter(Schedule.vol_id == volunteer.id,
               Schedule.date == schedule_date, Schedule.role_id == role.id).one() 

Make sure to add print statements for the methods.               