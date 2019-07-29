import logging


def get_olx_item_text(item):
    try:
        return {
            "name": item.find_all("strong")[0].text,
            "price": item.find_all("strong")[1].text
        }
    except:
        logging.error("Error in get_olx_item_text", exc_info=True)
        return None


def get_olx_items(soup):
    items_list = []
    items = soup.find_all("tr", {"class": "wrap"})
    items = [item for item in items if 'promoted-list' not in item.td.div.table['class']]
    for item in items:
        item_data = get_olx_item_text(item)
        if item_data:
            items_list.append(item_data)
    return items_list
