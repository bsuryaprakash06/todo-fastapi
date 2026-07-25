import sqlite3

DB_NAME = "tasks.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM tasks')
    count = cursor.fetchone()[0]
    
    if count == 0:
        sample_tasks = [
            ("Buy groceries", 0),
            ("Read documentation", 1),
            ("Write code", 0)
        ]
        cursor.executemany('''
            INSERT INTO tasks (title, done)
            VALUES (?, ?)
        ''', sample_tasks)
        
    conn.commit()
    conn.close()

init_db()
