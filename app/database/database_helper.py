import sqlite3

DATABASE_NAME = 'BSQ.db'

db_config = {
    'user': 'user',
    'password': 'myPassword',
    'host': 'localhost',
    'database' : 'BSQ'
}

def connect_db():
    return sqlite3.connect(DATABASE_NAME)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SOUND (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT UNIQUE NOT NULL,
        file_path TEXT UNIQUE NOT NULL
    );
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def set_sound(file_name, file_path):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO SOUND (file_name, file_path) VALUES (?, ?)
        ''', (file_name, file_path))
        
    #if name is already in use return a waring 
    except sqlite3.IntegrityError as e:
        cursor.close()
        conn.close()
        raise e 
    #otherwise return id of inserted record
    else:    
        conn.commit()
        # Ottieni l'ID appena inserito
        sound_id = cursor.lastrowid
        cursor.close()
        conn.close()
        # Restituisce l'ID associato al file_name
        return sound_id

def get_sound_by_id(sound_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM SOUND WHERE id = ?', (sound_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result
    
    
def get_sounds_list():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, file_name FROM SOUND')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_latest_id():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id) FROM SOUND ')
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0]

def get_sound_by_filename(file_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM SOUND WHERE file_name = ?', (file_name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    print(result)
    return result

def delete_sound_by_id(sound_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM SOUND WHERE id = ?', (sound_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
def delete_sound_by_filename(file_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM SOUND WHERE file_name = ?', (file_name,))
    conn.commit()
    cursor.close()
    conn.close()

# Checks if file exiss
# Param file_name
def check_sound_by_filename(file_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM SOUND WHERE file_name = ?', (file_name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return True
    else:
        return False


# Checks if file exiss
# Param id
def check_sound_by_id(id):  
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM SOUND WHERE id = ?', (id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return True
    else:
        return False    
