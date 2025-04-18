from constants import GenerateHelp, CommandInput

help = GenerateHelp([
    "Чтобы посмотреть все команды, используйте /help commands",
    "Чтобы узнать о команде, введите /{command_name} help"
])

def Execute(data: CommandInput) -> str:
    args = data["args"]
    send = data["send"]

    if len(args) > 1 and args[1] == "commands":
        return send("Все возможные команды:\n/" + "\n/".join(data["commands"].keys())).text

    return send(help).text