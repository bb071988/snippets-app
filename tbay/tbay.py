
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey,func,desc
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('postgresql://action:action@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
   
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable = False)
    password = Column(String, nullable = False)
    
    item_id = relationship("Item", backref = 'items') # AAAA
    bid_id = relationship("Bid", backref = 'bids') # BBBB
    
class Item(Base):
    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    owner_id = Column(Integer, ForeignKey("users.user_id"), nullable = False) # AAAA
#     bidder_id = Column(Integer, ForeignKey("bid.bid_id"), nullable = False) # CCCC

class Bid(Base):
    __tablename__ = "bid"
    
    bid_id = Column(Integer, primary_key=True)
    price = Column(Float, nullable = False)
    
    bidder_id = Column(Integer, ForeignKey("users.user_id"), nullable = False) # BBBBB
    
#     item_id = Column(Integer, ForeignKey("items.item_id"), nullable = False) # CCCC
    
    
Base.metadata.create_all(engine) # create the tables if they don't exist

# ********************************************  Create the users  ****************************

bob = User()
bob.user_name = "bob"
bob.password = "secret"
# bob.user_id = 1
# session.add(bob)
# session.commit()

dom = User()
dom.user_name = "dom"
dom.password = "secret"
# dom.user_id = 2

joe = User()
joe.user_name = "joe"
joe.password = "secret"
# joe.user_id = 3

session.add_all([bob,dom,joe])
session.commit()

# ******************** Bob auctions a baseball  *****************

baseball = Item()
baseball.item_id = 123
baseball.item_name = "newbaseball"
baseball.description = "almost new baseball"
baseball.owner_id = bob.user_id # ***** sets the owner of the baseball to be bob
session.add(baseball)
session.commit()

# dom bids on the baseball
dom_bid = Bid()
# dom_bid.bid_id = 1
dom_bid.bidder_id = dom.user_id
dom_bid.price = 8.50
session.add(dom_bid)
session.commit()

dom_bid2 = Bid()
# dom_bid2.bid_id = 2
dom_bid2.bidder_id = dom.user_id
dom_bid2.price = 10.50
session.add(dom_bid2)
session.commit()

# joe bids on the baseball
joe_bid = Bid()
# joe_bid.bid_id = 3
joe_bid.bidder_id = joe.user_id
joe_bid.price = 9.25
session.add(joe_bid)
session.commit()

joe_bid2 = Bid()
# joe_bid2.bid_id = 4
joe_bid2.bidder_id = joe.user_id
joe_bid2.price = 12.25
session.add(joe_bid2)
session.commit()


# Run a few queries
users = session.query(User).all() # Returns a list of all of the user o
items = session.query(Item).all()
bids = session.query(Bid).all()

max_qry = session.query(func.max(Bid.price).label("max_price"))  ##  Need help from sam here

# from sqlalchemy.sql import func
# qry = session.query(func.max(Score.score).label("max_score"), 
#                     func.sum(Score.score).label("total_score"),
#                     )
# #qry = qry.group_by(Score.some_group_column)
# for _res in qry.all():
#     print _res

# print users
print "Printing users"
for u in users:
    print u.user_name, u.user_id

print "Printing items"
for i in items:
    print i.item_name
    
print "Printing bids"
for b in bids:
    print b.bid_id,b.price
    
print "Max bid"
bid_list = session.query(Bid.price).all()
max_price = max(bid_list)
print bid_list
print max_price[0]  #didn't expect this to return a tuple

# get max from db using orderby
max_order = session.query(Bid.price, Bid.bid_id).order_by(desc(Bid.price)).all()
print max_order
print max_order[0][0]


# # Keeping the following items for future reference.

# # Finds the user with the primary key equal to 1
# session.query(User).get(1)

# # Returns a list of all of the usernames in ascending order
# session.query(User.user_name).order_by(User.user_name).all()

# # Returns the description of all of the basesballs
# session.query(Item.description).filter(Item.item_name == "baseball").all()

# # Return the item id and description for all baseballs which were created in the past.  Remember to import the datetime object: from datetime import datetime
# session.query(Item.item_id, Item.description).filter(Item.item_name == "baseball", Item.start_time < datetime.utcnow()).all()

# # deleting a user
# user = session.query(User).first()
# session.delete(user)
# session.commit()

# updating the user
# user = session.query(User).first()
# user.user_name = "bobupdated"
# session.commit()

# football = Item()
# football.name = "newfootball"
# football.description = "brand new football"
# session.add(football)
# session.commit()


# # Returns the first user
# user1 = session.query(User).first()
# print user1
# print user1.user_name





