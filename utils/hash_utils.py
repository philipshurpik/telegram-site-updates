import hashlib


def get_hash(item_string):
    hashlib.md5(item_string.encode()).hexdigest()
