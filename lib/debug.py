#!/usr/bin/env python3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Volunteer, Role, Schedule, volunteer_role, Validate
import ipdb;

engine = create_engine('sqlite:///volunteers.db')
Session = sessionmaker(bind=engine)
session = Session()


if __name__ == '__main__':
    ipdb.set_trace()

