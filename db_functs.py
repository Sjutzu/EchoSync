import os
import sqlite3

databaseDir = os.path.join(os.getcwd(), '.dbs')
appDatabase = os.path.join(databaseDir, 'app_db.db')

def createDBorTable(tbName: str):
    #print(databaseDir)
    connection = sqlite3.connect(appDatabase)
    cursor = connection.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {tbName} (song TEXT)""")
    connection.commit()
    connection.close()

def addSongToTable(song :str, table :str, database = appDatabase):
    connection = sqlite3.connect(appDatabase)
    cursor = connection.cursor()
    cursor.execute(f"""INSERT INTO {table} VALUES (?)""", (song,))
    connection.commit()
    connection.close()