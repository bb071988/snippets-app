import logging
import sys
import argparse
import psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")


def like_find(like_string):
    
    print "printing likestring {}".format(like_string)
    logging.info("find a like snippet")
    with connection, connection.cursor() as cursor:
        cursor.execute("select * from snippets where message like %s ",('%like_string%', ))
#         cursor.execute("select * from snippets where message like '%test%'") # this works
        row = cursor.fetchall()
# select * from table where prescription like '%cowbell%'
   
    logging.debug("Snippets retrieved successfully.")
    print row
    return row


def catalog():
    logging.info("Listing all the snippets")
#     print ("im in the catalog function")
    with connection, connection.cursor() as cursor:
        cursor.execute("select keyword from snippets order by keyword")
        row = cursor.fetchall()

   
    logging.debug("Snippets retrieved successfully.")
    return row
    
def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()

    with connection, connection.cursor() as cursor:
            cursor.execute("insert into snippets values (%s, %s)", (name,snippet))
            #row = cursor.fetchone()
   
    logging.debug("Snippet stored successfully.")
    return name, snippet

#Using a cursor as a context manager

def get(name):
    """Retrieve the snippet with a given name.
    If there is no such snippet...
    Let the user know that there was no such snippet
    Returns the snippet.
    """
    
    logging.info("Getting snippet for {!r}".format(name))
    with connection, connection.cursor() as cursor:
            cursor.execute("select message from snippets where keyword=%s", (name,))
            row = cursor.fetchone()
    
    if row:  
        #connection.commit()
        logging.debug("Snippet retrieved successfully.")
        return row[0], name # returns the first element in the tuple that cursor.execute creates and cursor.fetchone returns
    else:
        print "No such snippet in the database"
        return "Search Error", name
    
        
def main():
    """Main function"""
    
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
#    arguments = parser.parse_args(sys.argv[1:])

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the catalog
    logging.debug("Constructing catalog subparser")
    cat_parser = subparsers.add_parser("cat", help="Show catalog of snippet")
#     cat_parser.add_argument("name", help="The name of the snippet")
#     put_parser.add_argument("snippet", help="The snippet text")

    
    # Subparser for the like command
    logging.debug("Constructing put subparser")
    like_parser = subparsers.add_parser("like", help="find a snippet")
    like_parser.add_argument("like_string", help="string we are searching for in the snippet")
     
        
    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")


    # Subparser for the get command
    logging.debug("Constructing Get subparser")
    get_parser = subparsers.add_parser("get", help="Get a snippet from storage")
    get_parser.add_argument("name", help="The name of the snippet")

    
    arguments = parser.parse_args(sys.argv[1:])
    
    # Convert parsed arguments from Namespace to dictionary
    
    arguments = vars(arguments)
    #print arguments
    command = arguments.pop("command")
    
    #print command

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    
    elif command == "get":
        print("")
        snippet = get(**arguments)
        print "Retrieved snippet: {!r} based on search term {!r}".format(snippet[0],snippet[1])
        
    elif command =="cat":  ########### ask Sam about this.  Should we use enumerate here?
        row = catalog()
        for name, snippet in enumerate(row):
            print snippet[0]
            
    elif command =="like":
        
        row = like_find(**arguments)
#         row = like(like_string)
        for name, snippet in enumerate(row):
            print snippet[1], snippet[0]
        

if __name__ == "__main__":
    main()

