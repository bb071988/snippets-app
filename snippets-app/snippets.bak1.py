import logging
import sys
import argparse
import psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")



def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    command = "insert into snippets values (%s, %s)" 
    cursor.execute(command, (name, snippet))
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet


def get(name):
    """Retrieve the snippet with a given name.
    If there is no such snippet...
    Let the user know that there was no such snippet
    Returns the snippet.
    """
    
    logging.info("Getting snippet for {!r}".format(name))
    cursor=connection.cursor()
    command = "select message from snippets where keyword=(%s)"
    cursor.execute(command, (name,))  #*** *** *** syntax here seems to want cursor.execute to come in as a list[] or need to keep comma after name
    row = cursor.fetchone()
    
    if not row:  
        connection.commit()
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
        
    
    

if __name__ == "__main__":
    main()

