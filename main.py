from parse import parse
import json

id_flat_g = 0
info = []

'''Вебсайт:
    1) Надеждинское полесье
    2) Восточный луч Медленно
    3) ДаВинчи Групп Быстро
    4) ЖК Акватория Медленно
    5) Брусника Медленно
    6) Оазис
    7) Ласточка
    8) Владстрой'''

for website in range(1, 9):
    info, id_flat = parse(website, id_flat_g)
    id_flat_g += (id_flat - id_flat_g)

with open('info_flats.json', 'w', encoding='utf-8') as file:
    json.dump(info, file, ensure_ascii=False)