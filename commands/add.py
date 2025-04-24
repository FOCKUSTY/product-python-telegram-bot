from constants import SPACE, CommandInput, GenerateHelp, REQUIRED_PRODUCT_OPTIONS, PRODUCT_OPTIONS

import env
import database

KEYS = PRODUCT_OPTIONS.keys()

def Execute(data: CommandInput):
    send = data["send"]
    args = data["args"]
    message = data["message"]

    if not f"{message.from_user.id}" in env.get("ADMINS_TELEGRAM_IDS").split(","):
        return send("У Вас нет доступа к этой команде")
    
    if len(args) == 1:
        return send("Вы должны указать следующие значения:\n" + ", ".join(PRODUCT_OPTIONS) + "\n\nИз которых обязательные:\n" + " ,".join(REQUIRED_PRODUCT_OPTIONS))
    
    options = {}
    args.pop(0)

    for i in args:
        arg = i.split("=")

        if not arg[0] in KEYS:
            send(f"Ключа {arg[0]} не существует, попробуйте:\n" + ", ".join(KEYS))
            continue

        options[arg[0]] = arg[1].replace(SPACE[0], SPACE[1])

    keys = options.keys()

    for i in REQUIRED_PRODUCT_OPTIONS:
        if not i in keys:
            return send(f"Ключ {i} обязательный. Все обязательные ключи:\n" + ", ".join(REQUIRED_PRODUCT_OPTIONS))

    product = database.Product(
        name=options[PRODUCT_OPTIONS["name"]],
        price=options[PRODUCT_OPTIONS["price"]],
        count=options[PRODUCT_OPTIONS["count"]],
        address=options[PRODUCT_OPTIONS["address"]],
        description=(options[PRODUCT_OPTIONS["description"]] if PRODUCT_OPTIONS["description"] in options else ""),
        image_url=(options[PRODUCT_OPTIONS["image_url"]] if PRODUCT_OPTIONS["image_url"] in options else ""),
    )

    return send("Продукт создан\n" + product.__repr__())

    
help = GenerateHelp([
    f"Вы должны указать несколько значений ({len(PRODUCT_OPTIONS)}):\n{", ".join(PRODUCT_OPTIONS)}"
    + f"\n\nИз которых обязательные ({len(REQUIRED_PRODUCT_OPTIONS)}):\n{", ".join(REQUIRED_PRODUCT_OPTIONS)}",

    "Чтобы указать значения, используйте формат: {name}={value}, например: name=Вишневый или price=500.00",
    "Чтобы указать несколько значений, вводите их через пробел: /add name=Вишневый price=500.00 count=15 address=ул.-Пушкина-д.-Колотушкина",
    f'Чтобы указать значения, в который есть пробел (допустим адрес), то замените пробел на "{SPACE[0]}" (пример выше)'
])