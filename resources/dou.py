import logging


def get_dou_item(item):
    try:
        return {
            "title": item.find("div", {'class': 'title'}).text.replace('\n\n', ' ').replace('\t', '')
                .replace('\n', ' ').replace('\xa0', ' ').replace('  ', ' ').strip(),
            "company": item.find("a", {'class': 'company'}).text.strip(),
            "link": item.find("a", {'class': 'vt'}).attrs['href'].split('?')[0].strip(),
            "text": item.find("div", {'class': 'sh-info'}).text.replace('\n\n', ' ').replace('\t', '').replace('\xa0', ' ').strip()
        }
    except:
        logging.error("Error in get_dou_item", exc_info=True)
        return None


def get_dou_items(soup):
    items_list = []
    items = soup.find_all("li", {'class': 'l-vacancy'})
    for item in items:
        item_data = get_dou_item(item)
        if item_data:
            items_list.append(item_data)
    return items_list


def get_tracked_fields():
    return {
        "keys": ["company", "title"],
        "values": None
    }


def get_new_message(item):
    return f"{item['title']}\n\n{item['text'][0:200]}...\n{item['link']}"


def get_example_link():
    return "https://jobs.dou.ua/vacancies/?category=Front%20End"
