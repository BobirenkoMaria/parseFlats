from parse import parse
import json

info = []

'''website = int(input('Вебсайт: \n'
                '1) Надеждинское полесье\n'
                '2) Восточный луч\n'
                '3) ДаВинчи Групп\n'
                '4) ЖК Акватория \n'
                '5) Брусника\n'
                '6) Оазис\n'
                '7) Ласточка\n'
                '8) Владстрой\n'))'''

for website in range(2, 9):
    info.append(parse(website))
    print('check')

with open('info_flats.json', 'w', encoding='utf-8') as file:
    json.dump(info, file, ensure_ascii=False)