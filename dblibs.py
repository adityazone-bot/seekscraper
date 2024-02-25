import sqlite3
import os

dbFile = os.path.dirname(os.path.realpath(__file__)) + os.sep + "seek.db"

def openDB():
    connection = sqlite3.connect(dbFile)
    try:
        connection.execute('''CREATE TABLE JOB
                        (JOBID INT PRIMARY KEY NOT NULL,
                        TITLE TEXT NOT NULL,
                        URL TEXT NOT NULL,
                        COMPANY TEXT NOT NULL,
                        LOCATION TEXT NOT NULL,
                        STATUS TEXT NOT NULL,
                        DATEPOSTED TEXT,
                        TYPE TEXT,
                        DESCRIPTION TEXT,
                        SUMMARY TEXT,
                        KEYWORDS TEXT);
                    ''')           #STATUS will be PHASE1, PHASE2, PHASE3
    except Exception as err:
        if not 'already exists' in str(err):
            raise

    return connection

def executeQuery(connection, query):
    cursor = connection.execute(query)
    return cursor

def closeDB(connection):
    connection.close()