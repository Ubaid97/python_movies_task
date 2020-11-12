import pyodbc # used to establish db connection
import pandas # used to read csv file

class Manager:

    def __init__(self):
        # the following block of code is used to establish a pyodbc connection to northwind database
        self.server = "databases1.spartaglobal.academy"
        self.database = "Northwind"
        self.username = "SA"
        self.password = "Passw0rd2018"
        self.northwind_connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        # server name - database name - username and password is required to connect to pyodbc
        self.cursor = self.northwind_connection.cursor()
        self.table_data = pandas.read_csv("imdbtitles.csv") # reading imdbtitles csv file using pandas
        # declaring a dataframe (a data structure) with column names from the csv file read in line 15
        self.df = pandas.DataFrame(self.table_data, columns=['titleType', 'primaryTitle', 'originalTitle', 'isAdult', 'startYear', 'endYear', 'runtimeMinutes', 'genres'])


    # function used to create a table using the data from the csv file
    def create_table(self):
        # executes sql command to create a table with the columns in the csv file
        self.cursor.execute("CREATE TABLE ubaid_imdb_table ( "
                            "titleType varchar(200),"
                            "primaryTitle varchar(200),"
                            "originalTitle varchar(200), "
                            "isAdult bit,"
                            "startYear varchar(4),"
                            "endYear varchar(4),"
                            "runtimeMinutes varchar(4),"
                            "genres varchar(200)"
                            ") ")
        self.northwind_connection.commit() # commits the sql command executed in line 22 to the northwind db


    # function used to insert data from the csv file into the table
    def insert_in_table(self):
        # for loop iterating over the dataframe (see line 17) and inserting each row of data into the create table
        for row in self.df.itertuples(): # .itertuples() creates a tuple for every row in self.df (line 17), for loop then iterates over these rows
            # executes sql command to insert data from self.df.itertuples() into the table
            self.cursor.execute("INSERT INTO ubaid_imdb_table (titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row.titleType, row.primaryTitle, row.originalTitle, row.isAdult, row.startYear, row.endYear, row.runtimeMinutes, row.genres)
        self.northwind_connection.commit() # commits the sql command executed in line 39 to the northwind db


    # function that prints out all movies in the table
    def all_movies(self):
        # executes sql query to select all entries with the title type 'movie'
        movie_list = self.cursor.execute("SELECT * FROM ubaid_imdb_table WHERE titleType = 'movie'").fetchall()
        # fetchall() gets all the selected entries and stores them in the declared variable
        # for loop iterating over the list of movies (from line 48) and printing all the rows one by one
        for row in movie_list:
            print(row)


    # function for searching a movie by title. takes in the title as an argument from the user
    def search_movie(self, movie_name):
        # executes sql query to select all entries whose primary title matches the title passed in by the user
        searched_movie = self.cursor.execute(f"SELECT * FROM ubaid_imdb_table WHERE primarytitle = '{movie_name}'").fetchall()
        # for loop iterating over the list of movies (from line 58) and printing all the rows one by one
        for row in searched_movie:
            print(row)


    # function for adding movies to the table in the db. takes values for all the table columns as arguments to be passed in by user
    def add_movies(self, title_type, primary_title, original_title, is_adult, start_year, end_year, runtime_minutes, genre):
        # executes sql command to insert the values passed in by the user ino the table
        self.cursor.execute(
            "INSERT INTO ubaid_imdb_table (titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            title_type, primary_title, original_title, is_adult, start_year, end_year,
            runtime_minutes, genre)
        self.northwind_connection.commit() # commits the sql command executed in line 67 to the northwind db

        # sql query to select movie(s) with the primary title that the user passed in for the movie they added to the table
        added_movie = self.cursor.execute(f"SELECT * FROM ubaid_imdb_table WHERE primarytitle = '{primary_title}'").fetchall()
        # for loop iterates over the list of added movies (from 74) and prints them one by one
        for row in added_movie:
            print(row)


test_run = Manager() # creating instance of Manager class
# test_run.create_table() # calling function to create a table. once created comment out this line - otherwise will just create the same table again
# test_run.insert_in_table() # calling function to insert data from csv file into created table. comment out this line after calling function once
test_run.all_movies() # calling function to print out all the movies in the table
test_run.search_movie('Bigfoot') # calling function to print out the table entry for the movie Bigfoot
# test_run.add_movies('movie', 'hello world', 'hello world', False, '2020', '2020', '60', 'sci-fi') # calling function to add a movie by passing in values for each column - only run this line once for each movie to be added







