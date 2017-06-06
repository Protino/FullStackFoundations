from database_setup import Puppy, Shelter
from sqlalchemy import create_engine, desc, asc, func
from sqlalchemy.orm import sessionmaker
from pprint import pprint
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from operator import itemgetter

def printPuppies(puppies):
    for name,attr in puppies:
        print ('{0}\t\t\t\t{1}'.format(name,attr))

engine = create_engine('sqlite:///puppies.db')
Session = sessionmaker(bind=engine)
session = Session()

def query1():
    puppies = session.query(Puppy).order_by(asc(Puppy.name)).all()
    print '=================================='
    print 'All puppy names in ascending order'
    print '=================================='
    print '\n'.join(x.name for x in puppies)

def query2():
    limit = date.today() + relativedelta(months=-5)
    puppies = session.query(Puppy.name,Puppy.dateOfBirth).\
                        filter(Puppy.dateOfBirth>limit).\
                        order_by(desc(Puppy.dateOfBirth)).all()
    print '======================================================='
    print 'Puppies less than 6 months old sorted by youngest first'
    print '======================================================='

    printPuppies(puppies)

def query3():
    puppies = session.query(Puppy.name,Puppy.weight).order_by(asc(Puppy.weight)).all()

    print '============================================'
    print 'All puppy names ordered by ascending weights'
    print '============================================'
    printPuppies(puppies)

def query4():
    result = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
    for item in result:
        print item[0].id, item[0].name, item[1]

if __name__ == '__main__':
    #query1()
    #query2()
    #query3()
    query4()
