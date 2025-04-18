from telebot.types import Message

import telebot
import env

from downloader import Download

bot = telebot.TeleBot(env.get("TELEGRAM_TOKEN"))

COMMANDS = Download()

@bot.message_handler(content_types=['text'])
def start(message: Message):
    command_name = message.text.split(" ")[0].split("/")[1]
    args = message.text.split(" ")

    if len(args) > 1 and args[1] == "help" and command_name != "help":
        return bot.send_message(message.from_user.id, COMMANDS[command_name][1])

    try:
        command = COMMANDS[command_name][0]

        try:
            command({
                "send": lambda text: bot.send_message(message.from_user.id, text),
                "args": args,
                "message": message,
                "bot": bot,
                "commands": COMMANDS
            })
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