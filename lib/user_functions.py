
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import Volunteer

engine = create_engine('sqlite:///volunteers.db')
Session = sessionmaker(bind=engine)
session = Session()

def username_input():
        username = input("\nEnter the username or x to quit: ")
        username = username.strip()
        return username     

def clear_screen():
        print("\n" * 40)

def user_exist(username):
        volunteer = session.query(Volunteer).filter(Volunteer.username==username).first() 
        return volunteer 

def keep_output_on_screen():
        user_input = input("\nEnter to exit: ") 
        return user_input

