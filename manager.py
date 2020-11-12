import pyodbc
import csv
import pandas

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
        self.table_data = pandas.read_csv("imdbtitles.csv")
        self.df = pandas.DataFrame(self.table_data, columns=['titleType', 'primaryTitle', 'originalTitle', 'isAdult', 'startYear', 'endYear', 'runtimeMinutes', 'genres'])

    def create_table(self):


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
        self.northwind_connection.commit()

    def insert_in_table(self):
        for row in self.df.itertuples():
            self.cursor.execute("INSERT INTO ubaid_imdb_table (titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row.titleType, row.primaryTitle, row.originalTitle, row.isAdult, row.startYear, row.endYear, row.runtimeMinutes, row.genres)
        self.northwind_connection.commit()

    def all_movies(self):
        movie_list = self.cursor.execute("SELECT * FROM ubaid_imdb_table WHERE titleType = 'movie'").fetchall()
        # print(movie_list)
        for row in movie_list:
            print(row)

    def search_movie(self, movie_name):
        searched_movie = self.cursor.execute(f"SELECT * FROM ubaid_imdb_table WHERE primarytitle = '{movie_name}'").fetchall()
        for row in searched_movie:
            print(row)

    def add_movies(self, title_type, primary_title, original_title, is_adult, start_year, end_year, runtime_minutes, genre):
        self.cursor.execute(
            "INSERT INTO ubaid_imdb_table (titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            title_type, primary_title, original_title, is_adult, start_year, end_year,
            runtime_minutes, genre)
        self.northwind_connection.commit()

        added_movie = self.cursor.execute(f"SELECT * FROM ubaid_imdb_table WHERE primarytitle = '{primary_title}'").fetchall()
        for row in added_movie:
            print(row)


test_run = Manager()
# test_run.create_table()
# test_run.insert_in_table()
test_run.all_movies()
test_run.search_movie('Bigfoot')
# test_run.add_movies('movie', 'hello world', 'hello world', False, '2020', '2020', '60', 'sci-fi')
test_run.search_movie('hello world')







