import traceback
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from logger_config import logger
import chardet


HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.64', 'accept': 'application/json, text/plain, */*'}

info = []
website = None
houseFloorFlat_num = [0, 0, 0]


id_flat = 0
def set_info(name, flat, floor, house, area, price, busy):
    global id_flat

    info.append({
        'id': int(id_flat),
        'name': str(name),
        'flatNum': int(flat),
        'floorNum': int(floor),
        'houseNum': int(house),
        'area': float(area),
        'price': int(price),
        'busy': str(busy)
    })
    id_flat += 1


def get_html(url, params=None):
    try:
        r = requests.get(url, headers=HEADERS, params=params)
    except requests.exceptions.ConnectionError:
        return None
    return r


def get_url(page=None, house=None, floor=None, flat=None):
    url = ''

    if website == 1:
        url = f'https://зимаюжная.рф/#/profitbase/house/96{house}/facades?propertyId=9619{flat}&floorNumber=1&filter=property.status:AVAILABLE'
    elif website == 2:
        url = f'https://vlzu.ru/apartments?page={page}'
    elif website == 3:
        url = f'https://davinchigroup.ru/flats/#/complex?page={page}'
    elif website == 4:
        url = f'https://акватория-жк.рф/dom{house}/etazh{floor}/vasha-kvartira{flat}'
    elif website == 5:
        url = f'https://brusnika-dom.ru/product/квартира-{flat}-дом-{house}/'
    elif website == 6:
        url = f'https://oasis-dom.ru/room/{flat}'
    elif website == 7:
        url = f'https://lasto4ka.ru/select/floor/1/{flat}#flat'
    elif website == 8:
        url = f'https://sabaneeva22a.ru/flat-info/?{flat}'

    print(chardet.detect(url))
    return url


main_info = [0,0,0,0]
def get_content(html):
    if website == 1:
        soup = BeautifulSoup(html, 'html.parser')

        items = soup.find('div', class_='apartment-info ng-star-inserted')

        busy = items.find('div', class_='apartment-info__status')
        flat = items.find('div', class_='apartment-info__title')
        area = items.find('div', class_='main-specs__item')
        floor = items.find('div', class_='main-specs__value ng-star-inserted')
        price = items.find('div', class_='ellipsis ng-star-inserted')

        set_info('Надеждинское полесье', flat, floor, houseFloorFlat_num[0], area, price, busy)

    elif website == 2:
        soup = BeautifulSoup(html, 'html.parser')

        floors = soup.find_all('a', class_="CardBox_link__3yLNB CardBox_def_card__1X_8R")

        for floor in floors:
            price = floor.find_all('span')
            houseNum_floor = floor.find_all('div', class_='CardBox_value__29byo')
            main_info[0] = houseNum_floor[1].get_text()
            main_info[1] = houseNum_floor[2].get_text()
            main_info[2] = ((price[1].get_text()).split()[0]).replace(' ', '')
            main_info[3] = price[2].get_text()

            website_parse(f'https://vlzu.ru{floor.get("href")}')

    elif website == 3:
        text = html.split('\n')

        i = 0
        while i < len(text):

            set_info('ДаВинчи Групп', text[i+4][1:], text[i+5],
                     text[i+1].split()[-1], text[i+6].split()[0].replace(',', '.'),
                     text[i+2].replace(' ', '')[:-1], "Свободно")

            i += 7

    elif website == 4:
        soup = BeautifulSoup(html, 'html.parser')

        info_card = soup.find('div', class_='info-card')
        info_card = info_card.find_all('dd')
        area = (info_card[0].get_text()).split()[0]
        price = (info_card[1].get_text()).replace(' ', '')[:-2]
        busy = 'Свободно'

        if price == 'бро':
            price = 0
            busy = 'Бронь'
        elif price == 'прода':
            price = 0
            busy = 'Продано'
        elif price == 'позапро':
            price = 0
            busy = 'По запросу'

        set_info('Акватория', houseFloorFlat_num[2], houseFloorFlat_num[1],
                 houseFloorFlat_num[0], area, price, busy)

    elif website == 5:
        soup = BeautifulSoup(html, 'html.parser')

        price = soup.find('span', class_='woocommerce-Price-amount amount')
        price = (price.get_text()).replace(' ', '')[:-1]
        info_flat = soup.find_all('td', class_='woocommerce-product-attributes-item__value')
        area = info_flat[5].get_text()
        floor = info_flat[4].get_text()
        busy = soup.find('p', class_='stock')

        set_info('Брусника', houseFloorFlat_num[2], floor[:-1], houseFloorFlat_num[0], area[:-1], price[:-1], busy.get_text())

    elif website == 6:
        soup = BeautifulSoup(html, 'html.parser')

        info_card = soup.find('div', class_='block__item')
        info_card = info_card.find_all('div', class_='text_with_icon__text')

        floor = info_card[0].get_text()
        area = info_card[2].get_text()

        price = None
        busy = None
        if len(info_card) > 3:
            price = info_card[3].get_text()
            busy = 'Свободно'
        else:
            price = 0
            busy = soup.find('p', class_='title title--lvl3').get_text()

        set_info('Оазис', houseFloorFlat_num[2], floor.split()[1], 1, area.split()[1],
                 (price.split(':')[1]).replace(' ', '')[:-1] if price != 0 else price, busy)

    elif website == 7:
        soup = BeautifulSoup(html, 'html.parser')

        info_card = soup.find_all(class_='v-list-item__content')

        floor = soup.find('div', class_='d-flex justify-center')
        floor = floor.find('h1').get_text()

        busy = info_card[5].get_text().replace(' ', '')
        area = info_card[7].get_text()
        price = info_card[9].get_text().replace(' ', '')

        set_info('Ласточка', houseFloorFlat_num[2], floor.split()[0],
                 1, area.split()[0], price[:-1] if price != '-' else 0, busy)

    elif website == 8:
        soup = BeautifulSoup(html, 'html.parser')

        flat = soup.find('li', class_='p10__flat-num')
        flat = flat.find_all('span')
        flat = flat[1].get_text()

        floor = soup.find('li', class_='p10__flat-floor')
        floor = floor.find_all('span')
        floor = floor[1].get_text()

        price = soup.find('li', class_='p10__flat-price')
        price = (price.get_text())[10:-5].replace(' ', '')

        area = soup.find('li', class_='p10__flat-area')
        area = area.find_all('span')[1].get_text()

        set_info('Владстрой', flat, floor, 1, area.split()[0], price, 'Свободно' if int(price) != 0 else 'Занято')


def max_page():
    last_page = 0
    URL = get_url(1)

    html = None
    while html == None:
        html = get_html(URL)

        soup = BeautifulSoup(html.text, 'html.parser')

        if website == 2:
            pages = soup.find_all('li', class_='Paginator_li__1PhzI')
            last_page = pages[-1].get_text()
        elif website == 3:
            html = get_html_with_driver(URL)
            pages = soup.find_all('li', class_='page-item')
            last_page = pages[-1].get_text()

    return int(last_page)


def get_website_content(html):
    soup = BeautifulSoup(html, 'html.parser')

    all_info = soup.find('ul', class_='ApartmentInfo_prop__192RT')

    apartment = all_info.find_all('div', class_='ApartmentInfo_prop_value__1bijC')[2]
    apartment = apartment.get_text()

    set_info('Восточный луч', apartment, main_info[0], main_info[1],
             str(main_info[2]).replace(',', '.'), str(main_info[3]).replace(' ', ''), 'Свободно')


def website_parse(url):
    html = None
    while html == None:
        html = get_html(url)
        try:
            if html.status_code == 200:
                get_website_content(html.text)
        except AttributeError:
            print("Connection refused in website_parse")


def parse(num, id_flat_g):
    global id_flat
    global cycle_times
    global houseFloorFlat_num
    try:
        setup(id_flat_g, num)

        if website == 0:
            return info

        elif website == 1:
            for house in range(1, 3):
                num_house = 140 if house == 1 else 657

                houseFloorFlat_num[0] = house
                for flat in range(1, 112):
                    URL = get_url(house=num_house, flat=flat + 712)

                    parser(URL)

        elif website == 2:
            for page in range(1, max_page() + 1):
                URL = get_url(page)

                parser(URL)

        elif website == 3:
            for page in range(1, 3):
                URL = get_url(page)

                text = get_html_with_driver(URL)
                get_content(text)

        elif website == 4:
            for house in range(1, 3):
                flats_count = 1
                for floor in range(2, 26):
                    last_flat = flats_count
                    if floor == 2:
                        flats_count += 12
                    else:
                        flats_count += 13

                    for flat in range(last_flat, flats_count):
                        houseFloorFlat_num = [house, floor, flat]

                        URL = get_url(house=house, floor=floor, flat=flat)

                        parser(URL)

        elif website == 5:
            for house in range(1, 8):
                count_flat = 0
                if house == 1:
                    count_flat = 21
                elif house == 2:
                    count_flat = 36
                elif house == 3:
                    count_flat = 16
                elif house == 4:
                    count_flat = 36
                elif house == 5:
                    count_flat = 24
                elif house == 6:
                    count_flat = 24
                elif house == 7:
                    count_flat = 24

                for flat in range(1, count_flat + 1):
                    houseFloorFlat_num = [house, 0, flat]

                    URL = get_url(house=house, flat=flat)

                    parser(URL)

        elif website == 6:
            for flat in range(1, 232):
                houseFloorFlat_num[2] = flat

                URL = get_url(flat=flat)

                parser(URL)

        elif website == 7:
            for flat in range(1, 11):
                houseFloorFlat_num = [0, 0, flat]

                URL = get_url(flat=flat)
                html = get_html_with_driver(URL)
                get_content(html)

        elif website == 8:
            for flat in range(1, 172):
                houseFloorFlat_num[2] = flat

                URL = get_url(flat=flat)

                parser(URL)

    except Exception as ex:
        #logger.error("Connection refused. Check website that you parse")
        logger.error(traceback.format_exc())

    cycle_times = 0
    return info, id_flat


def get_html_with_driver(url):
    driver = webdriver.Chrome(executable_path='chromedriver')
    html = None

    driver.get(url=url)
    time.sleep(5)
    while True:
        try:
            if website == 7:
                html = driver.page_source
                break

            elif website == 3:
                str = 'return document.querySelector("#code_block-26-235 > kvg-widget").shadowRoot.' \
                      'querySelector("#app > div.widget__wrapper > div.widget__content > ' \
                      'div > section > div > div.flats > div.flats__content > div")'
                html = (driver.execute_script(str)).text
                break
        except Exception as ex:
            checking_cycle()
            time.sleep(1)

    driver.close()
    driver.quit()

    return html


def parser(URL):
    html = None

    while html == None:
        html = get_html(URL)
        try:
            if html.status_code == 200:
                get_content(html.text)

        except AttributeError:
            checking_cycle()
            logger.debug(f'URL: {URL} - website code response: {html.status_code}')


cycle_times = 0
def checking_cycle():
    global cycle_times
    cycle_times += 1

    if cycle_times >= 10:
        parse(0, 0)


def setup(id_flat_l, num):
    global website
    global id_flat

    id_flat = id_flat_l
    website = num
