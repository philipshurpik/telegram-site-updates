def load_user_config():
    try:
        from .user_config import Config
    except ImportError:
        from .base_config import Config
    return Config()


def init():
    cfg = load_user_config()
    return cfg


config = init()
