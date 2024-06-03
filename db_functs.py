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

def addSongToTable(song :str, table :str):
    connection = sqlite3.connect(appDatabase)
    cursor = connection.cursor()
    cursor.execute(f"""INSERT INTO {table} VALUES (?)""", (song,))
    connection.commit()
    connection.close()

def deleteAllSongsFromTable(table: str):
    connection = sqlite3.connect(appDatabase)
    cursor = connection.cursor()
    cursor.execute(f"""DELETE FROM {table} """)
    connection.commit()
    connection.close()

def deleteSongFromTable(song: str,table: str):
    connection = sqlite3.connect(appDatabase)
    cursor = connection.cursor()
    cursor.execute(
        f"""DELETE FROM {table} WHERE
        ROWID = (SELECT min(ROWID) from favourites
        WHERE song = "{song}" )"""
    )
    connection.commit()
    connection.close()

def fetchAllSongsFromTable(table: str):
    connection = sqlite3.connect(appDatabase)
    cursor = connection.cursor()
    cursor.execute(f"""SELECT song FROM {table} """)
    songData = cursor.fetchall()
    data = [song[0] for song in songData]
    connection.commit()
    connection.close()

    return data

def getPlaylistTables():
    try:
        connection = sqlite3.connect(appDatabase)
        cursor = connection.cursor()
        cursor.execute(f"""SELECT * from sqlite_master WHERE type = 'table';""")
        tableNames = cursor.fetchall()
        tables = [tableName[1] for tableName in tableNames]

        return tables
    except Exception as e:
        print(f"Error getting table names {e}")
    finally:
        connection.close()

def deleteTable(table: str):
    connection = sqlite3.connect(appDatabase)
    cursor = connection.cursor()
    cursor.execute(f"""DROP TABLE {table} """)
    connection.commit()
    connection.close()