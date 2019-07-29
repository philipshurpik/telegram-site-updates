def load_user_config():
    try:
        from .user_config import config
    except ImportError:
        from .demo_config import config
    return config


def init():
    cfg = load_user_config()
    print(f"Config keys: {list(cfg.keys())}")
    return cfg


config = init()
