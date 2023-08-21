#The Scheduler

***The Scheduler*** born out of the need for a more robust volunteer scheduling system for my church. The app manages the scheduling of the volunteer for the church by enabling a user to add, modify, and delete a volunteer and/or schedule and query the schedule by date and/or username. Ideally only people with admin privileges will be able to make any changes to the schedule. However, everyone will be able to query the schedule by date and username. Currently there are no admin privileges set for the app so everyone has full access.

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

## Volunteer

- primary key
- first name
- last name
- username 
- email
- phone
- week
- assigned

## Role
- id primary key
- prayer 
- greeter
- welcome table 
- usher

## volunter_Roles
- vol_id foreign key
- rol_id foreign key

The Volunteer Table consist of one relatational

Volunteer_Roles is a join or association table that joins Volunteers and Roles. It consist of a primary key and 

