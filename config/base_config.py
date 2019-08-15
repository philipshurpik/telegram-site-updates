class Config:
    users_folder = "data/users"
    items_folder = "data/items"
    error_timeout = 60
    poll_timeout = 60 * 30
    telegram_token = 'TOKEN'
    available_resources = ["olx", "lun", "dou"]
    users = {
        'USER_ID': {
            "olx": [
                "https://www.olx.ua/elektronika/telefony-i-aksesuary/mobilnye-telefony-smartfony/"
            ],
            "lun": [
                "https://www.lun.ua/uk/%D0%BE%D1%80%D0%B5%D0%BD%D0%B4%D0%B0-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80-%D0%BA%D0%B8%D1%97%D0%B2"
            ],
            "dou": [
                "https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Front%20End"
            ]
        }
    }
