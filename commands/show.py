import telebot

from typing import Literal
from constants import SPACE, SHOW_KEYS, GenerateHelp, CommandInput, BUTTONS

from database import get

KEYS: tuple[
    Literal['id'],
    Literal['name'],
    Literal['address'],
    Literal['page'],
] = tuple(list(SHOW_KEYS) + ["page"])

def Execute(data: CommandInput) -> str:
    args: list[str] = data["args"][1:len(data["args"])]
    send = data["send"]
    bot = data["bot"]
    message = data["message"]

    page = "1"

    keyboard = telebot.types.InlineKeyboardMarkup()
    buttonNext = telebot.types.InlineKeyboardButton(text="===>", callback_data=BUTTONS["next_page"])
    buttonPrevious = telebot.types.InlineKeyboardButton(text="<===", callback_data=BUTTONS["previous_page"])
    keyboard.add(buttonPrevious, buttonNext)

    if len(args) == 0:
        products = ""

        datas, _ = get(["page=" + page], True)

        for p in datas:
            product = f"Товар: {p.name}. Цена: {p.price}. Количество: {p.count}. Идентификатор: {p.id}. Адрес: {p.address}"
            products = products + "\n" + product + "\n"

        return bot.send_message(
            message.from_user.id,
            f"page: {page}\nНаши товары:\n{products}\nЧтобы перейти на следующую, введите: /show page={int(page)+1}",
            reply_markup=keyboard
        )

    if len(args) == 1 and args[0].isdigit():
        args = ["id="+args[0]]

    for arg in args:
        if not arg.split("=")[0] in KEYS:
            return send(f"Неправильный ввод значения, попробуйте:\n/show {KEYS[0]}=\n/show {KEYS[1]}=\n/show {KEYS[2]}=")

    products, page = get(args, True)
    output = ""

    for p in products:
        data = "\n".join([
            f"Товар: {p.name}",
            f"Идентификатор: {p.id}",
            f"Цена: {p.price}",
            f"Количество: {p.count}",
            f"Адрес: {p.address}"
        ])

        if not p.description == "": data = data + f"\n\nОписание:\n{p.description}"
        if not p.image_url == "": data = data + f"\n\nСсылка на картинку: {p.image_url}"

        output = output + "\n" + data + "\n"

    if not f"page={page}" in args:
      return bot.send_message(message.from_user.id, " ".join([f"page={page}"] + args) + "\n" + output, reply_markup=keyboard)
    
    return bot.send_message(message.from_user.id, " ".join(args) + "\n" + output, reply_markup=keyboard)

help = GenerateHelp([
    "Используйте /show help чтобы показать это меню",
    "Используйте /show для просмотра всех наших товаров",
    "Используйте /show {id} для просмотра конкретного товара (Пример: /show 1)",
    "Используйте /show {method}={value} для просмотра конкретного товара. Примеры:\n/show id=1\n/show name=Виноград\n/show address=г.-Уфа-ул.-Пушкина-56",
    f"Используйте \"{SPACE[0]}\" вместо привычного пробела для его поставления (/show address=г.-Уфа-ул.-Пушкина-56)",
    "Все возможные методы сортировки: " + ", ".join(KEYS),
    "Используйте /show page={page}, чтобы вывести определенную страницу (Пример: /show page=1 или /show name=Виноград page=1)"
])