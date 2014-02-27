import sqlite3
import datetime

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

def create_account(username, password, password_verify):
    #see if user already exists
    query = """SELECT username FROM users where username = ?"""
    DB.execute(query, (username,))
    check_username = DB.fetchone()
    if check_username != None:
        return 1
    elif hash(password) != hash(password_verify):
        return 2
    else:
        query = """INSERT INTO users (username, password) VALUES (?, ?)"""
        DB.execute(query, (username, password))
        CONN.commit()
        return "New user"


def get_userid_by_name(username):
    #write function to take username, look up user_id
    query = """SELECT id FROM users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()
    return row[0]

def get_username_by_id(userid):
    query = """SELECT username FROM users WHERE id = ?"""
    DB.execute(query, (userid,))
    row = DB.fetchone()
    return row[0]

def get_wall_posts(user_id):
    query = """SELECT id, content, created_at, author_id FROM wall_posts WHERE owner_id = ? ORDER BY created_at DESC"""
    DB.execute(query, (user_id,))
    rows = DB.fetchall()
    posts = []
    for row in rows:
        post = {"author": get_username_by_id(row[3]), "date": row[2], "content": row[1]}
        posts.append(post)
    print posts
    return posts

def post_to_wall(wall_owner,author_id,content):
    created_at = datetime.datetime.now()
    created_at = created_at.strftime("%Y-%m-%d %H:%M")
    owner_id = get_userid_by_name(wall_owner)
    query = """INSERT INTO wall_posts (owner_id, author_id, created_at, content) VALUES (?, ?, ?, ?)"""
    DB.execute(query, (owner_id,author_id, created_at, content))
    CONN.commit()

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    print create_account("liz", "gurlplz", "gurlplz")
    while command != "quit":
        pass

    CONN.close()

if __name__ == "__main__":
    main()

