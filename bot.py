from telebot.types import Message
from typing import Callable

import telebot
import env

from downloader import Download

bot = telebot.TeleBot(env.get("TELEGRAM_TOKEN"))

COMMANDS = Download()

def SendMessageByMessage(message: Message) -> Callable[[str], Message]:
    def send(text: str) -> Message:
        return bot.send_message(message.from_user.id, text)

    return send

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
            data = command({
                "send": sendToUser,
                "args": args,
                "message": message,
                "bot": bot,
                "commands": COMMANDS
            })

            print(f"Выполнена команда {command_name} пользователей {message.from_user.id}")
            print("Результат выполнения:")
            print(data)
        except Exception as error:
            print(error)
    except:
        all_commands = ""

        for i in list(COMMANDS.keys()):
            all_commands = all_commands + "\n/" + i

        bot.send_message(message.from_user.id, 'Команда не распознана, возможные команды:' + all_commands)
    

if __name__ == "__main__":
    print("Включение бота")
    bot.infinity_polling()