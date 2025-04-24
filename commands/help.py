from constants import GenerateHelp, CommandInput

help = GenerateHelp([
    "Чтобы посмотреть все команды, используйте /help commands",
    "Чтобы узнать о команде, введите /{command_name} help",
    "Или можете ввести /help {command_name}"
])

def Execute(data: CommandInput) -> str:
    args = data["args"]
    send = data["send"]
    commands = data["commands"]

    if len(args) > 1 and args[1] in commands:
        return send(commands[args[1]][1])

    if len(args) > 1 and args[1] == "commands":
        return send("Все возможные команды:\n/" + "\n/".join(data["commands"].keys()))

    return send(help)