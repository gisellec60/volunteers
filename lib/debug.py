#!/usr/bin/env python3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Volunteer, Role, Schedule, volunteer_role
from datetime import datetime, date
from sqlalchemy import Table, Boolean, ForeignKey, Column, Integer, String, MetaData, select


if __name__ == '__main__':
    engine = create_engine('sqlite:///volunteers.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    import ipdb; ipdb.set_trace()

