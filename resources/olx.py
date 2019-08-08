import logging


def get_olx_item(item):
    try:
        link = item.find_all('a')[0].attrs['href'].split('#')[0]
        return {
            "id": link.split('/')[-1].split('.')[0],
            "name": item.find_all("strong")[0].text,
            "price": item.find_all("strong")[1].text if len(item.find_all("strong")) > 1 else None,
            "link": link,
            "photo": item.find_all('img')[0].attrs['src'].split(';')[0] if len(item.find_all('img')) > 0 else None,
        }
    except:
        logging.error("Error in get_olx_item", exc_info=True)
        return None


def get_olx_items(soup):
    items_list = []
    items = soup.find_all("tr", {"class": "wrap"})
    items = [item for item in items if 'promoted-list' not in item.td.div.table['class']]
    for item in items:
        item_data = get_olx_item(item)
        if item_data:
            items_list.append(item_data)
    return items_list


def get_tracked_fields():
    return {
        "keys": ["id"],
        "values": ["name", "price"]
    }


def get_new_message(item):
    return f"{item['name']}\n\n>>> {item['price']}\n\n{item['photo']}\n\n{item['link']}"

def get_message_update(item, diff):
    diff_fields = [d['field'] for d in diff]
    update_text = "Обновлено!\n"
    if 'price' in diff_fields:
        idx = diff_fields.index("price")
        update_text = f"Новая цена: {diff[idx]['after']}, старая: {diff[idx]['before']}\n\n"
    return f"{update_text}{item['name']}\n\n>>> {item['price']}\n\n{item['photo']}\n\n{item['link']}"
