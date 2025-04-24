import sqlite3
import random

from constants import SPACE

connection = sqlite3.connect('test.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
id INTEGER PRIMARY KEY,
name STRING NOT NULL,
price FLOAT NOT NULL,
count INTEGER NOT NULL,
address TEXT NOT NULL,
description TEXT,
image_url TEXT
)
''')

connection.commit()

INDEXES = {
    "id": 0,
    "name": 1,
    "price": 2,
    "count": 3,
    "address": 4,
    "description": 5,
    "image_url": 6
}

class Product:
    def create(self):
        data = cursor.execute("INSERT INTO products (name, price, count, address, description, image_url) VALUES (?, ?, ?, ?, ?, ?)", (self.name, self.price, self.count, self.address, self.description, self.image_url))
        connection.commit()

        return data

    def __init__(self, name: str, price: float, address: str, count: int, description: str, image_url: str, id: int|None = None, create: bool = False):
        self.name = name
        self.price = price
        self.count = count
        self.address = address
        self.description = description
        self.image_url = image_url
        
        if id: self.id = id
        if create: self.create()

    def __repr__(self):
        return f"<Product(name='{self.name}', price='{self.price}', count='{self.count}', address='{self.address}')>"

def concatTuples(tupleOne: tuple, tupleTwo: tuple):
    return tuple(list(tupleOne) + list(tupleTwo))

def fromArrayToObject(product: tuple[int, str, float, int, str, str, str]):
    return Product(
        name=product[INDEXES["name"]],
        price=product[INDEXES["price"]],
        count=product[INDEXES["count"]],
        address=product[INDEXES["address"]],
        description=product[INDEXES["description"]],
        image_url=product[INDEXES["image_url"]],
        id=product[INDEXES["id"]],
        create=True,
    )

def fromArrayToSQL(values: list[str], start: str="WHERE", pageExists: bool = False):
    global page
    page = 1

    sql = start
    datas = []

    for v in values:
        data = v.split("=")

        if pageExists and data[0] == "page":
            page = int(data[1])
            continue

        datas.append(data[1].replace(SPACE[0], SPACE[1]))
        sql = sql + f" {data[0]} = ?"

    if sql == "WHERE": sql = ""

    return (sql, datas, page)

def updateArray(values: list[str], update: list[str]):
    updates = {}
    output = []

    for v in update:
        up = v.split("=")
        updates[up[0]] = up[1]

    for value in values:
        v = value.split("=")

        if v[0] in updates:
            if "-" in updates[up[0]] or "+" in updates[up[0]]:
                output.append(f"{v[0]}={int(v[1]) + int(updates[up[0]])}")
            else:
                output.append(f"{v[0]}={updates[up[0]]}")
        else:
            output.append(f"{v[0]}={v[1]}")

    return output

def get(values: list[str], toProductObject: bool = False) -> tuple[list[Product], int]:
    global page
    count = 5
    
    sql = fromArrayToSQL(values, "WHERE", True)
    promt = f"SELECT * FROM products {sql[0]} LIMIT {(page-1)*count}, {count}"
    page = sql[2]

    if int(page) <= 1:
        data = cursor.execute(f"SELECT * FROM products {sql[0]} LIMIT {(page-1)*count}, {count}", sql[1]).fetchall()

        if toProductObject:
            products = []

            for product in data:
                products.append(fromArrayToObject(product))

            return (products, 1)
    
        return (data, 1)

    print("Запрос к БД:\n"+promt, sql[1])
    data = cursor.execute(promt, sql[1]).fetchall()

    if toProductObject:
        products = []

        for product in data:
            products.append(fromArrayToObject(product))

        return (products, page)

    return (data, page)

def delete(id: int):
    data = cursor.execute("DELETE FROM products id = ?", (id))
    connection.commit()
    
    return data

def update(id: int, values: list[str]):
    sql = fromArrayToSQL(values, "SET", False)

    data = cursor.execute(f"UPDATE products {sql[0]} WHERE id = ?", (concatTuples(sql[1], (id))))
    connection.commit()

    return data

if __name__ == "__main__":
    datas = {
        "name": [
            "Клубника",
            "Виноград",
            "Яблоко",
            "Груша",
            "Розмарин"
        ],
        "price": [
            499.99,
            1499.99,
            799.99,
            199.99,
            999.99,
            2000
        ],
        "count": [
            100,
            50,
            35,
            10,
            5,
            160
        ],
        "ул": [
            "Пушкина",
            "Пустоты",
            "Безработицы",
            "Проспект Октября",
            "Полевая",
            "Солнечная",
            "Информируемая",
            "Округ Фейри",
            "Мизонтропов",
            "Магов"
        ],
        "г": [
            "Уфа", "Астрахань",
            "Москва", "Санкт\\Петербург",
            "Саратов", "Якутск",
            "Иркутск", "Нижний Новгород",
            "Киров", "Челябинск",
            "Пенза", "Чистый",
            "Банитея", "Подшляпный"
        ],
        "д": [
            "Колотушкина", "666",
            "123", "23/2",
            "Крутой", "9",
            "23", "1", "Вали",
            "Фикусов", "Победы"
        ]
    }

    def getRandom(array: list):
        return array[random.randint(0, len(array)-1)]

    length = 0
    length = 30

    for i in range(length):
        address = f"г. {getRandom(datas["г"])} ул. {getRandom(datas['ул'])} д. {getRandom(datas['д'])}"

        Product(
            name=getRandom(datas["name"]),
            price=getRandom(datas["price"]),
            count=getRandom(datas["count"]),
            address=address,
            description="",
            image_url="",
            id=None,
            create=True
        )
    
    # products = get(["page=6"], False)
    # for p in products: print(p)

    pass