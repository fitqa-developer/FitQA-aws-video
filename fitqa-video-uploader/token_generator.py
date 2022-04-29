import string
import random

_TOKEN_LENGTH = 20

def _random_character(length: int) -> str:
  random_pool = string.ascii_letters + string.digits
  return ''.join(random.choice(random_pool) for _ in range(length))

def random_character_with_prefix(prefix: str) -> str:
  return prefix + _random_character(_TOKEN_LENGTH - len(prefix))