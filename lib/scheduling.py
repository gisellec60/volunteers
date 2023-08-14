#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import   Volunteer, Role, Schedule, join_table

import click

import ipdb; ipdb.set_trace()
@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')

def start():
    import ipdb; ipdb.set_trace()
    print("Welcome to Schedulier \n")
    print("Add Volunteer")
    print("Delete Volunteer")
    user_input = input("Pick one")

    handle_user_input(user_input)

    def handle_user_input(input):
        import ipdb; ipdb.set_trace()
        is_number = input.isdigit()
        if is_number:
           handle_add_volunteer(input)

    def handle_add_volunteer():
        pass

if __name__ == '__main__':
    engine = create_engine('sqlite:///volunteers.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    hello()

    