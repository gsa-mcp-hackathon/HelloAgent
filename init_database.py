"""Create the fictional HelloAgent demo inventory without overwriting records."""
import sqlite3
from contextlib import closing
from inventory_repository import DEFAULT_DB

RECORDS = [
    ('HR Portal', 'Human Resources', 'Active', 'Python', 'Microsoft', 'Approved'),
    ('Legacy Reports', 'IT Operations', 'Retirement candidate', 'Java', 'Microsoft', 'Not Approved'),
]


def initialize_database(path=DEFAULT_DB):
    with closing(sqlite3.connect(path)) as conn:
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS applications (
                name TEXT PRIMARY KEY NOT NULL,
                owner TEXT,
                status TEXT,
                technology TEXT,
                vendor TEXT,
                approval_status TEXT
            )''')
            conn.executemany('''INSERT INTO applications
                (name, owner, status, technology, vendor, approval_status)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(name) DO NOTHING''', RECORDS)
    return path


if __name__ == '__main__':
    print(f'Demo database initialized: {initialize_database()}')
