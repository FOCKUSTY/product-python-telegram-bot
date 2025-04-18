from typing import TypedDict, Any, Callable, Final
from telebot.types import Message
import telebot

SPACE = ("-", " ")
SHOW_KEYS = ("id", "name", "address")

DEFAULT_SPLITTER: Final[str] = "\n\n"

COMMANDS_DIR: Final[str] = "commands"

class CommandInput(TypedDict):
    send: Callable[[str], Any]
    args: tuple[str]
    message: Message
    bot: telebot.TeleBot
    commands: dict[str, tuple[Callable[[Message], Any], Callable[[str, Any], Any]]]

class ProductOptions(TypedDict):
    name: str
    price: float
    count: int
    address: str
    description: str | None
    image_url: str | None

PRODUCT_OPTIONS: Final[ProductOptions] = {
    "name": "name",
    "price": "price",
    "count": "count",
    "address": "address",
    "description": "description",
    "image_url": "image_url"
}

REQUIRED_PRODUCT_OPTIONS: Final[tuple[str]] = (
    PRODUCT_OPTIONS["name"],
    PRODUCT_OPTIONS["price"],
    PRODUCT_OPTIONS["count"],
    PRODUCT_OPTIONS["address"]    
)

NO_REQUIRED_PRODUCT_OPTIONS: Final[tuple[str | None]] = (
    PRODUCT_OPTIONS["description"],
    PRODUCT_OPTIONS["image_url"]    
)

def GenerateHelp(args: list[str], splitter: str = DEFAULT_SPLITTER):
    return splitter.join(args)