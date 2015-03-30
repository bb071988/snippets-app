from datetime import datetime
from tbay import User, Item, Bid, session

bob = User()
bob.username = "bob"
bob.password = "secret"
session.add(bob)
session.commit()

dom = User()
dom.username = "dom"
dom.password = "secret"
session.add(dom)
session.commit()

baseball = Item()
baseball.name = "newbaseball"
baseball.description = "almost new baseball"
session.add(baseball)
session.commit()

football = Item()
football.name = "newfootball"
football.description = "brand new football"
session.add(football)
session.commit()


# Returns a list of all of the user objects
users = session.query(User).all() # Returns a list of all of the user o

print users
for u in users:
    print u.username

# Returns the first user
user1 = session.query(User).first()
print user1
print user1.username

# Finds the user with the primary key equal to 1
session.query(User).get(1)

# Returns a list of all of the usernames in ascending order
session.query(User.username).order_by(User.username).all()

# Returns the description of all of the basesballs
session.query(Item.description).filter(Item.name == "baseball").all()

# Return the item id and description for all baseballs which were created in the past.  Remember to import the datetime object: from datetime import datetime
session.query(Item.id, Item.description).filter(Item.name == "baseball", Item.start_time < datetime.utcnow()).all()

# deleting a user
user = session.query(User).first()
session.delete(user)
session.commit()

# updating the user
user = session.query(User).first()
user.username = "bobupdated"
session.commit()



# def print_query():
#     query_list=[]
#     query_list = session.query(User).all() # Returns a list of all of the user objects
#     return query_list
    
# print print_query()




