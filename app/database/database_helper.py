import sqlite3

DATABASE_NAME = 'system_db.db'

db_config = {
    'user': 'user',
    'password': 'myPassword',
    'host': 'localhost',
    'database' : 'system_db'
}

def connect_db():
    return sqlite3.connect(DATABASE_NAME)

# Creates table at startup if not already existing
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        PRAGMA foreign_keys = 1;
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SOUND (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        position INTEGER UNIQUE NOT NULL,
        file_name TEXT UNIQUE NOT NULL,
        file_path TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,
        CONSTRAINT FK_SOUND_CATEGORY FOREIGN KEY (category) REFERENCES CATEGORY(category_name)
    );''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CATEGORY (
        category_name TEXT PRIMARY KEY
    );''')
    conn.commit()
    cursor.close()
    conn.close()

# Query to set the correct sound position
def set_position():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''PRAGMA foreign_keys = 1''')
    cursor.execute('''
        SELECT MIN(s1.position + 1) AS first_free_position
        FROM (
		SELECT position
		FROM sound
		UNION
		SELECT 0
	) s1
        LEFT JOIN sound s2 ON s1.position + 1 = s2.position
        WHERE s2.position IS NULL
    ''')

    first_free_position = cursor.fetchone()[0]  # Ottieni il primo valore della tupla
    cursor.close()
    conn.close()

    return first_free_position


# Inserts sound into given position
def set_sound(position: int, file_name: str, file_path: str, category: str):
    conn = connect_db()
    cursor = conn.cursor()
    if position is None:
       check_position=set_position()
    else:
       check_position=position
    try:
        cursor.execute('''PRAGMA foreign_keys = 1''')
        cursor.execute('''
        INSERT OR REPLACE INTO SOUND (position, file_name, file_path, category) VALUES (?, ?, ?, ?)
        ''', (check_position, file_name, file_path, category)); 
    #if file name or/and position is already in use return an error 
    except sqlite3.IntegrityError as e:
        print(e)
        cursor.close()
        conn.close()
        raise e 

    #otherwise return position of inserted record
    else:    
        conn.commit()
        cursor.close()
        conn.close()
        return check_position

# Inserts category into database
def set_category(category: str):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''PRAGMA foreign_keys = 1''')
        cursor.execute('INSERT OR REPLACE INTO CATEGORY (category_name) VALUES (?)', (category,))
    except sqlite3.IntegrityError as e:
        print(e)
        cursor.close()
        conn.close()
        raise e
    conn.commit()    
    cursor.close()
    conn.close()
    return 

# Retrieves the sound by position
def get_sound_by_pos(position: int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''PRAGMA foreign_keys = 1''')
    cursor.execute('SELECT * FROM SOUND WHERE position = ?', (position,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

    
# Retrieves all sounds    
def get_sounds_list():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''PRAGMA foreign_keys = 1''')
    cursor.execute('SELECT * FROM SOUND')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Retrieves all categories 
def get_category_list():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''PRAGMA foreign_keys = 1''')
    cursor.execute('SELECT * FROM CATEGORY')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Retrieves all sound of the input category
def get_sounds_list_by_category(category: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''PRAGMA foreign_keys = 1''')
    cursor.execute('''SELECT * FROM SOUND WHERE category = ?''', (category,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Checks whether the given category exists  
def category_is_valid(category: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''PRAGMA foreign_keys = 1''')
    cursor.execute('''SELECT * FROM CATEGORY WHERE category_name = ?''', (category,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if result:
        return True	
    else:
        return False

def get_latest_position():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''PRAGMA foreign_keys = 1''')
    cursor.execute('SELECT MAX(position) FROM SOUND ')
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0]

# Retrieves sound by input value
def get_sound_by_filename(file_name: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''PRAGMA foreign_keys = 1''')
    cursor.execute('SELECT * FROM SOUND WHERE file_name = ?', (file_name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# Deletes sound at input position
def delete_sound_by_pos(position: int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''PRAGMA foreign_keys = 1''')
    cursor.execute('DELETE FROM SOUND WHERE position = ?', (position,))
    conn.commit()
    cursor.close()
    conn.close()

# Deletes sound of given filename    
def delete_sound_by_filename(file_name: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''PRAGMA foreign_keys = 1''')
    cursor.execute('DELETE FROM SOUND WHERE file_name = ?', (file_name,))
    conn.commit()
    cursor.close()
    conn.close()

# Deletes category of given name
def delete_category(category: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''PRAGMA foreign_keys = 1''')
    cursor.execute('DELETE FROM CATEGORY WHERE category_name = ?', (category,))
    conn.commit()
    cursor.close()
    conn.close()

