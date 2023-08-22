# The Scheduler

***The Scheduler*** was born out of the need for a more robust volunteer scheduling system for my church. The app manages the scheduling of the volunteer for the church by enabling a user to add, modify, and delete a volunteer and/or schedule and query the schedule by date and/or username. Ideally only people with admin privileges will be able to make any changes to the schedule. However, everyone will be able to query the schedule by date and username. Currently there are no admin privileges set for the app so everyone has full access.

The Scheduler consist of 4 tables: 
- Volunteer
- Schedule
- Role
- Volunteers_Roles

![Alt Text](pictures/tables.png)

## Schedule

- id primary Key
- date 
- swapp_id 
- vol_id foreign key
- role_id foreign key

Because Schedule has a one-to-many relationship with Volunter and Role foreign keys were create for both tables to manage the relationship

## Volunteer

- id primary key
- first name
- last name
- username 
- email
- phone
- week
- assigned

 Besides a primary key the volunteer table has two relational fields. *roles* is used for managing the relationship between the Role and Volunteer tables through the association table, *Volunteers_Roles* 

*schedules* is use is used to manage the relationship to between Schedule and Volunteer tables. 

- roles = relationship('Role', secondary='volunteer_role',
                          back_populates='volunteers')
- schedules = relationship('Schedule', backref=backref('volunteer'))

## Role
- id primary key
- prayer 
- greeter
- welcome table 
- usher

Like the Volunteer table the Role table has two relational fields. *volunteers* which manages the relatationship between Role and Volunteer through the association table *Volunteer_Roles*

*schedules* is used to manage the relationship between Schedule and the Role tables.

- volunteers = relationship('Volunteer', secondary='volunteer_role',
                          back_populates='roles')
- schedules = relationship('Schedule', backref=backref('role'))

## volunter_Roles
- vol_id foreign key
- rol_id foreign key

Volunteer_Roles is an association table that manages the relationship between Volunteers and Roles. 

The Scheduler is a CLi app so the user interacts with it from the command line. The cli file that envokes the scheduler is...wait for it...*scheduling.py*

![Alt Text](pictures/scheduler.png)