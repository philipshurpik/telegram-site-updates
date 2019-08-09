import logging

import requests
from bs4 import BeautifulSoup


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
    link, photo = _get_actual_link_and_photo(item)
    return f"{item['name']}\n\n>>> {item['price']}\n\n{item['text'][0:200]}...\n{photo}\n{link}"


def get_message_update(item, diff):
    link, photo = _get_actual_link_and_photo(item)
    diff_fields = [d['field'] for d in diff]
    update_text = "Обновлено!\n"
    if 'price' in diff_fields:
        idx = diff_fields.index("price")
        update_text = f"Новая цена: {diff[idx]['after']}, старая: {diff[idx]['before']}\n\n"
    return f"{update_text}{item['name']}\n\n>>> {item['price']}\n\n{photo}\n{link}"


def _get_actual_link_and_photo(item):
    try:
        response = requests.get(item['link'], headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'lxml')
        actual_link = soup.find_all('a')[-1].attrs['href']
        response = requests.get(actual_link, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'lxml')
        imgs = soup.find_all('img')
        photo = next((img.attrs['src'] for img in imgs if ".jp" in img.attrs['src']), "")
        return actual_link, photo
    except:
        return item['link'], ""
