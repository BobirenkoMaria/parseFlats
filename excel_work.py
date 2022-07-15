import openpyxl

def set_worksheet():
    wb = openpyxl.open('TestCopy.xlsx', data_only=True)

    sheet = wb.active
    return sheet, wb


def input_to_worksheet(info):
    sheet, wb = set_worksheet()

    i = 0
    for line in range(2, len(info)+2):
        sheet[line][0].value = int(info[i]['flatNum'])
        sheet[line][1].value = int(info[i]['floorNum'])
        sheet[line][2].value = int(info[i]['houseNum'])
        sheet[line][3].value = float(info[i]['area'])
        sheet[line][4].value = int(info[i]['price'])
        sheet[line][5].value = info[i]['busy']

        i+=1

    is_open = True
    while is_open:
        try:
            wb.save('TestCopy.xlsx')
            is_open = False
        except PermissionError:
            print('Закройте эксель файл и нажмите Enter')
            input()
            is_open = True