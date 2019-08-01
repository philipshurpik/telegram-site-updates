import hashlib


def get_hash(item_string):
    return hashlib.md5(item_string.encode()).hexdigest()
