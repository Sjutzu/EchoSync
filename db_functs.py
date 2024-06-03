import os
import sqlite3

databaseDir = os.path.join(os.getcwd(), '.dbs')
appDatabase = os.path.join(databaseDir, 'app_db.db')

def createDBorTable(tbName: str):
    print(databaseDir)
    connection = sqlite3.connect(appDatabase)
    cursor = connection.cursor()
    cursor.execute(f"""CREATE TABLE {tbName} (song TEXT)""")
    connection.commit()
    connection.close()

