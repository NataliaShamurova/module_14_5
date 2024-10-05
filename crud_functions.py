import sqlite3 as sq


def initiate_db():
    db = sq.connect('database')
    cur = db.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL              
    )
    ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL               
        )
        ''')
    db.commit()
    db.close()


def add_product(product_data):
    db = sq.connect('database')
    cur = db.cursor()
    cur.execute('''INSERT INTO Products (title, description, price) VALUES (?, ?, ?)''', product_data)
    db.commit()
    db.close()


def get_all_products():
    db = sq.connect('database')
    cur = db.cursor()
    cur.execute('SELECT * FROM Products')
    products = cur.fetchall()
    db.close()

    return products


def add_user(username, email, age):
    db = sq.connect('database')
    cur = db.cursor()
    balance = 1000
    cur.execute('''INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)''',
                (username, email, age, balance))
    db.commit()
    db.close()


def is_included(username):
    db = sq.connect('database')
    cur = db.cursor()
    cur.execute('''SELECT * FROM Users WHERE username = ?''', (username,))
    result = cur.fetchall()

    db.commit()
    db.close()

    return bool(result)
