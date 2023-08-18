import string
import time
from random import choices, randint, randrange


def generate_authorization_code() -> str:
    time.sleep(randrange(1, 2))

    return str(randint(1000, 9999))


def generate_invite_code() -> str:
    code_length = 6
    code_source = string.digits + string.ascii_uppercase + string.ascii_lowercase

    return "".join(choices(code_source, k=code_length))
