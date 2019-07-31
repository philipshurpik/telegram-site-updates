import logging


def get_lun_item(item):
    try:
        return {
            "name": f'{item.select("div[title]")[0].text} | {" | ".join([x.text for x in item.find_all("li")])}',
            "price": item.select("div > div > div > div > div")[0].text,
            "text": item.select("div > div > div > div")[-1].text,
            "link": f"https://www.lun.ua{item.find_all('a')[0].attrs['href'].split('?')[0]}"
        }
    except:
        logging.error("Error in get_lun_item", exc_info=True)
        return None


def get_lun_items(soup):
    items_list = []
    items = soup.find("main").find("section").find_all("article")
    items = [item for item in items if len(item.select("div[title]")) > 0]
    for item in items:
        item_data = get_lun_item(item)
        if item_data:
            items_list.append(item_data)
    return items_list


def get_tracked_fields():
    return {
        "keys": ["name"],
        "value": "price"
    }
