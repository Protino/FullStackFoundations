from database_setup import Restaurant, MenuItem
from sqlalchemy import create_engine, desc, asc, func
from sqlalchemy.orm import sessionmaker
from operator import itemgetter

engine = create_engine('sqlite:///restaurantmenu.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()
