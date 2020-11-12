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

    def create_table(self):
        table_data = pandas.read_csv("imdbtitles.csv")
        df = pandas.DataFrame(table_data, columns = ['titleType', 'primaryTitle', 'originalTitle', 'isAdult', 'startYear', 'endYear', 'runtimeMinutes', 'genres'])

        self.cursor.execute("CREATE TABLE imdb_table ( "
                            "titleType varchar(200),"
                            "primaryTitle varchar(200),"
                            "originalTitle varchar(200), "
                            "isAdult number(1),"
                            "startYear int,"
                            "endYear int,"
                            "runtimeMinutes int,"
                            "genres varchar(200)"
                            ") ")

        for row in df.itertuples():
            self.cursor.execute("INSERT INTO imdb_table (titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row.titleType, row.primaryTitle, row.originalTitle, row.isAdult, row.startYear, row.endYear, row.runtimeMinutes, row.genres)
        self.northwind_connection.commit()

    def all_movies(self):
        movie_list = self.cursor.execute("SELECT * FROM imdb_table WHERE titleType=movie").fetchall()
        for row in movie_list:
            print(row)





