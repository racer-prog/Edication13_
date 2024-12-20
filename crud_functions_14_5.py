import sqlite3
import os

dir_prod = "img"
files = os.listdir(dir_prod)
quant_prod = len(files)
img_list = sorted(files)
vitamins = ['A','B','C','D','E','F','G','H','I','J','K']

connection = sqlite3.connect("db/product.db")

cursor = connection.cursor()

def db_pre():
    global cursor
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    product TEXT NOT NULL,
    descr TEXT NOT NULL,
    price INTEGER NOT NULL,
    img TEXT NOT NULL
    )
    ''')
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_product ON Products (product)")

def db_write():
    global cursor
    for i in range(quant_prod):
        cursor.execute("INSERT INTO Products (product, descr, price, img) VALUES (?,?,?,?)",
                       (f"Витамин {vitamins[i]}", "https://yandex.ru/search/?text=витамин"+str(vitamins[i]), (i+1)*100, f"img/{img_list[i]}"))

def db_read():
    connection = sqlite3.connect("db/product.db")
    cursor = connection.cursor()
    all_prod = {}
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    for p in products:
        all_prod[p[0]] = list(p[1:])

    # for i,j in zip(range(len(all_prod.values())), all_prod.values()):
    #      print(i, j)
    # print(len(all_prod))
    return all_prod



db_pre()
# db_write()
db_read()

connection.commit()
connection.close()