from typing import Any, Callable
from telebot.types import Message

from constants import COMMANDS_DIR

import os
import importlib

COMMANDS = list(filter(lambda x: x.endswith(".py"), os.listdir(COMMANDS_DIR)))

def Download() -> dict[str, list[Callable[[Message], Any], Callable[[str, Any], Any]]]:
    modules = {}

    for command in COMMANDS:
        name = command.split(".")[0]
        module = importlib.import_module(f"{COMMANDS_DIR}.{name}")
        modules[name] = [module.Execute, module.help]

    return modules

if __name__ == "__main__":
    commands = Download()

    for command in commands:
        print(command)
        print(commands[command])