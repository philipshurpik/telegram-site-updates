import logging


def get_lun_item(item):
    try:
        link = item.find_all('a')[0].attrs['href'].split('?')[0]
        return {
            "id": link.split('/')[-1],
            "name": f'{item.select("div[title]")[0].text} | {" | ".join([x.text for x in item.find_all("li")])}',
            "price": item.select("div > a > div")[-1].text,
            "text": item.select("div > div > div > div")[-1].text,
            "link": f"https://www.lun.ua{link}"
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
        "keys": ["id"],
        "values": ["name", "price"]
    }


def get_new_message(item):
    return f"{item['name']}\n\n>>> {item['price']}\n\n{item['text'][0:200]}...\n{item['link']}"


def get_message_update(item, diff):
    diff_fields = [d['field'] for d in diff]
    update_text = "Обновлено!\n"
    if 'price' in diff_fields:
        idx = diff_fields.index("price")
        update_text = f"Новая цена: {diff[idx]['after']}, старая: {diff[idx]['before']}\n\n"
    return f"{update_text}{item['name']}\n\n>>> {item['price']}\n\n{item['link']}"
