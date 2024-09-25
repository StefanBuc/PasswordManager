import sqlite3

connection = sqlite3.connect("logins.db")
cursor = connection.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS Logins (
    Website TEXT NOT NULL,
    Username TEXT NOT NULL,
    Password TEXT NOT NULL
)
'''

cursor.execute(create_table_query)
connection.commit()