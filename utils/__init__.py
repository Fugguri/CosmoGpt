import re
from .GPTService import GPTService
from .LavaService import LavaService
gpt = GPTService()


def find_email(text):
    # Регулярное выражение для поиска электронных почт
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Используем re.findall для поиска всех совпадений
    emails = re.match(email_regex, text)

    return emails.string


lava = LavaService()
__all__ = [
    "gpt",
    "lava",
    "find_email",
]
