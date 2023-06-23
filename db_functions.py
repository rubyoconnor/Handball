import sqlite3
import csv
import string #for strip


def run_commit_query(sql_query,values_tuple, file_path):
    """Run a query that makes a change to the database
    :param (str) sql_query: str
    :param (tuple) values_tuple: tuple (can be empty)
    :param (str) file_path: str
    :return: (bool) success or not
    """
    try:
        # try to connect to the database
        # if the path is valid and no database, one will be created
        conn = sqlite3.connect(file_path)
        # get a cursor which allows us to do things
        cursor = conn.cursor()
        # turn on foreign key check - will give an error
        # if you try to delete something without removing
        # foreign keys first
        conn.execute("PRAGMA foreign_keys = 1")
        print("connection successful")
        # execute the query
        cursor.execute(sql_query, values_tuple)
        # save the database
        conn.commit()
        print("Commit Query executed")
        # shut down the cursor
        cursor.close()
    except sqlite3.Error as error:
        # if something has gone wrong the error should print in the console
        print("Commit Error: {}".format(error))
        return False
    # if all okay, shut down the connection
    conn.close()
    print("sqlite connection is closed")
    return True


def run_search_query_tuples(sql_query,values_tuple, file_path, rowfactory=False):
    """Run a query
    :param (str) sql_query: str
    :param (tuple) values_tuple: tuple (can be empty)
    :param (path) file_path: str
    :param (bool) rowfactory: bool
    :return: (tuple) result
    """
    result = None
    try:
        db = sqlite3.connect(file_path)
        # will get multi dict rather than tuples, needs flask
        if rowfactory:
            db.row_factory = sqlite3.Row
        cursor = db.cursor()
        #print("connection successful")
        cursor.execute(sql_query,values_tuple)
        result = cursor.fetchall()
        #print("Search Query executed")
        cursor.close()
    except sqlite3.Error as error:
        print("Error running search query tuples: {}".format(error))
        return None
    db.close()
    if result is None:
        print("No search values were found")
    return result


def file_reader(f):
    """Read a csv file (may not be necessary, but here if needed
    :param (str) f: file path
    :return: (list) 2D list: each row of the csv file split up by cells
    """
    # holds all the data
    collected_data = []
    # get the file
    with open(f , mode='r', encoding='utf-8-sig') as csv_file:
        csv_read = csv.reader(csv_file, delimiter = "," , quotechar='"', quoting=csv.QUOTE_MINIMAL)
        count = 0
        # loop through the rows
        for row in csv_read:
            # add each row split and stripped as a list
            collected_data.append( [x.strip() for x in row] )
            count+=1
    print(count)
    # return the 2D list
    return collected_data


def execute_external_script(sql_script_path, db_path):
    """Read a sql file and use to create a database

    :param (str) sql_script_path: str (path to sql file)
    :param (str) db_path: str (path to db file)
    :return: bool
    """
    try:
        # connect to database (if it is not there it will be created)
        conn = sqlite3.connect(db_path)
        # the cursor allows us to do things with the database
        cursor = conn.cursor()
        #print("connection successful")
        # open and read the sql file
        sql_query = open(sql_script_path)
        sql_string = sql_query.read()
        # use the cursor to execute the script in the file
        cursor.executescript(sql_string)
        # commit (aka save) what has been done
        conn.commit()
        #print("Query executed")
        # shut down the cursor
        cursor.close()
    except sqlite3.Error as error:
        # if there is an error print it out in the console
        print("Error while executing sql: {}".format(error))
        # return False if another part of the program needs to know of the failure
        return False
    # all okay if we are here
    # shut down the connection
    conn.close()
    print("sqlite connection is closed")
    return True


if __name__ == "__main__":
    sql_path = 'data/create_db.sql'
    db_path = 'data/handball_db.sqlite'
    execute_external_script(sql_path,db_path)