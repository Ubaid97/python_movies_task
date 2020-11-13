import pyodbc
import pandas

class SecondIter():

    def __init__(self):
        # the following block of code is used to establish a pyodbc connection to northwind database
        self.server = "databases1.spartaglobal.academy"
        self.database = "Northwind"
        self.username = "SA"
        self.password = "Passw0rd2018"
        self.northwind_connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)
        # server name - database name - username and password is required to connect to pyodbc
        self.cursor = self.northwind_connection.cursor()
        self.read_movies_txt = pandas.read_csv("movies.txt") # reading the movies,txt file using pandas
        self.write_movies_txt = open("new_movies.txt", "w") # used to write into a new txt file
        # # declaring a dataframe (a data structure) with column names from the txt file
        self.df = pandas.DataFrame(self.read_movies_txt, columns=['title', 'genres'])

    # function used to create a table using sql server
    def create_table(self):
        # executes sql command to create a table with the columns in the txt file
        self.cursor.execute("CREATE TABLE txt_table ( "
                            "title varchar(200),"
                            "genres varchar(200)"
                            ") ")
        self.northwind_connection.commit()  # commits the sql command executed in line 22 to the northwind db

    # # function used to insert data from the txt file into the table
    def insert_in_table(self):
        # for loop iterating over the dataframe (see line 20) and inserting each row of data into the created table
        for row in self.df.itertuples():  # .itertuples() creates a tuple for every row in self.df (line 20), for loop then iterates over these rows
            # executes sql command to insert data from self.df.itertuples() into the table
            self.cursor.execute("INSERT INTO txt_table (title, genres) VALUES (?, ?)", row.title, row.genres)
        self.northwind_connection.commit()  # commits the result of the executed sql command to the northwind db

    # function used to load data from the db and print it out
    def load_from_db(self):
        # executes sql query to select all entries from the table
        movie_list = self.cursor.execute("SELECT * FROM txt_table").fetchall()
        # fetchall() gets all the selected entries and stores them in the declared variable
        # for loop iterating over the list of movies (from line 42) and printing all the rows one by one
        for row in movie_list:
            print(row)

    # function used to output data rom the db into a text file
    def output_to_txt(self):
        # executes sql query to select all entries from the table
        movie_list = self.cursor.execute("SELECT * FROM txt_table").fetchall()
        # fetchall() gets all the selected entries and stores them in the declared variable
        # for loop iterating over the list of movies and writing them into a new text file (see line 18)
        for row in movie_list:
            self.write_movies_txt.write(row)

        # for loop reading the new text file and printing its contents row by row
        for row in self.write_movies_txt.read():
            print(row)

test_run = SecondIter() # creating instance of the class
# test_run.create_table() # calling function to create table
test_run.insert_in_table() # calling function to insert data from txt file into table
# test_run.load_from_db() # calling function to load data from the table in the db and printing it out
# test_run.output_to_txt() # calling function to output data from the table in the db to a new txt file and printing the contents of the txt file