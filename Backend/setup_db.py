import sqlite3

DATABASE = 'candidates.db'

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    face_encoding BLOB NOT NULL
)
''')

conn.commit()
conn.close()

print("Database setup completed.")