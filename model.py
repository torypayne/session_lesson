import sqlite3

DB = None
CONN = None

ADMIN_USER="hackbright"
ADMIN_PASSWORD=5980025637247534551

#803096023

def authenticate(username, password):
    password_input = hash(password)
    print password_input
    query = """SELECT password, id FROM users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()
    DB_password = hash(row[0])
    if password_input == DB_password:
        return row[1]
    else:
        return None

def get_userid_by_name(username):
    #write function to take username, look up user_id
    pass

def get_username_by_id(userid):
    pass

def get_wall_posts(user_id):
    connect_to_db()
    query = """SELECT id, content, created_at, author_id FROM wall_posts WHERE owner_id = ? """
    DB.execute(query, (user_id,))
    rows = DB.fetchall()
    posts = {}
    for row in rows:
        posts[row[0]] = {"author": row[3], "date": row[2], "content": row[1]}
    print posts
    return posts
  

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        pass

    CONN.close()

if __name__ == "__main__":
    main()