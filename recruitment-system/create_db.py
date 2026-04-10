import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""
CREATE TABLE jobs(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
company TEXT,
description TEXT
)
""")

conn.execute("""
CREATE TABLE candidates(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT,
resume TEXT
)
""")

conn.execute("""
CREATE TABLE applications (
id INTEGER PRIMARY KEY AUTOINCREMENT,
candidate_id TEXT,
job_id TEXT,
status TEXT
)
""")

conn.execute("""
CREATE TABLE recruiters(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT
)
""")

conn = sqlite3.connect("database.db")
conn.execute("ALTER TABLE applications ADD COLUMN interview_date TEXT")
conn.commit()
conn.close()


print("Database Created Successfully")