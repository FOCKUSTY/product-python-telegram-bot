from telebot.types import Message, CallbackQuery
from typing import Callable

import telebot
import env

from database import updateArray, get

from downloader import Download
from constants import BUTTONS

bot = telebot.TeleBot(env.get("TELEGRAM_TOKEN"))

COMMANDS = Download()

def SendMessageByMessage(message: Message) -> Callable[[str], Message]:
    def send(text: str) -> Message:
        return bot.send_message(message.from_user.id, text)

    return send

def PageHandler(operator: str):
    def nextPage(call: CallbackQuery):
      args = updateArray(call.message.text.split("\n")[0].split(" "), [f"page={operator}1"])
      
      keyboard = telebot.types.InlineKeyboardMarkup()
      buttonNext = telebot.types.InlineKeyboardButton(text="===>", callback_data=BUTTONS["next_page"])
      buttonPrevious = telebot.types.InlineKeyboardButton(text="<===", callback_data=BUTTONS["previous_page"])
      keyboard.add(buttonPrevious, buttonNext)

      products, _ = get(args, True)
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
          if not p.image_url == "": data = data + f"\n\n Ссылка на картинку: {p.image_url}" 

          output = output + "\n" + data + "\n"
      
      return bot.send_message(call.message.chat.id, " ".join(args) + "\n" + output, reply_markup=keyboard).text
    
    return nextPage

@bot.message_handler(content_types=['text'])
def start(message: Message):
    command_name = message.text.split(" ")[0].split("/")[1]
    args = message.text.split(" ")
    sendToUser = SendMessageByMessage(message)

    print("Вызвана комнада " + command_name)

    if len(args) > 1 and args[1] == "help" and command_name != "help":
        return sendToUser(COMMANDS[command_name][1])

    try:
        command = COMMANDS[command_name][0]

        try:
            command({
                "send": sendToUser,
                "args": args,
                "message": message,
                "bot": bot,
                "commands": COMMANDS
            })

            print(f"Выполнена команда {command_name} пользователем {message.from_user.id}")
        except Exception as error:
            print(error)
    except:
        all_commands = ""

        for i in list(COMMANDS.keys()):
            all_commands = all_commands + "\n/" + i

        bot.send_message(message.from_user.id, 'Команда не распознана, возможные команды:' + all_commands)

@bot.callback_query_handler(func=lambda call: call.data == BUTTONS["next_page"])
def nextPage(call: CallbackQuery):
    PageHandler("+")(call)

@bot.callback_query_handler(func=lambda call: call.data == BUTTONS["previous_page"])
def previosPage(call: CallbackQuery):
    PageHandler("-")(call)

if __name__ == "__main__":
    print("Включение бота")
    bot.infinity_polling()