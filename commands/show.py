from constants import SPACE, SHOW_KEYS, GenerateHelp, CommandInput

from sqlalchemy import select
from database import ProductBase, session

import database

KEYS = SHOW_KEYS

def Execute(data: CommandInput):
    args = data["args"]
    send = data["send"]

    if len(args) == 1:
        products = ""

        for p in database.get(ProductBase):
            product = f"Товар: {p.name}. Цена: {p.price}. Количество: {p.count}. Идентификатор: {p.id}"
            products = products + "\n" + product + "\n"

        return send("Наши товары:\n" + products)

    whereclause = args[1].replace(SPACE[0], SPACE[1]).split("=")

    if not whereclause[0] in KEYS and not whereclause[0].isdigit():
        return send(f"Неправильный ввод значения, попробуйте:\n/show {KEYS[0]}=\n/show {KEYS[1]}=\n/show {KEYS[2]}=")

    first = whereclause[0] if not whereclause[0].isdigit() else "id"
    second = whereclause[1] if whereclause[0] in KEYS else whereclause[0]
    products = list(session.scalars(select(ProductBase).where(eval(f"ProductBase.{first}") == second)).all())

    for p in products:
        data = "\n".join([
            f"Товар: {p.name}",
            f"Идентификатор: {p.id}",
            f"Цена: {p.price}",
            f"Количество: {p.count}",
            f"Адрес: {p.address}"
        ])

        if not p.description == "": data = data + f"\n\nОписание:\n{p.description}"
        if not p.image_url == "": data = data + f"\n\n Ссылка на картинку: {p.image_url}" 

        send(data)

    return

help = GenerateHelp([
    "Используйте /show help чтобы показать это меню",
    "Используйте /show для просмотра всех наших товаров",
    "Используйте /show {id} для просмотра конкретного товара (Пример: /show 1)",
    "Используйте /show {method}={value} для просмотра конкретного товара. Примеры:\n/show id=1\n/show name=Виноград\n/show address=г.-Уфа-ул.-Пушкина-56",
    f"Используйте \"{SPACE[0]}\" вместо привычного пробела для его поставления (/show address=г.-Уфа-ул.-Пушкина-56)",
    "Все возможные методы сортировки: " + ", ".join(KEYS)
])