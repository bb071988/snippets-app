###################  do all the sqlalchemy setup engine - sesson - base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://action:action@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

###########################  import the items we need.

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

# from declare_guitars import Base, session
from datetime import datetime

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    passport = relationship("Passport", uselist=False, backref="owner")

class Passport(Base):
    __tablename__ = 'passport'
    id = Column(Integer, primary_key=True)
    issue_date = Column(Date, nullable=False, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    
Base.metadata.create_all(engine) ######## super important to create the tables if they don't exist  

bob = Person(name="bob")
passport = Passport()
bob.passport = passport

session.add(bob)
session.commit()

print bob.passport.issue_date
print passport.owner.name