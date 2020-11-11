def message_parser(json):
    text = ''
    for lesson, note in json.items():
        if not note or note == '':
            note = 'Заданий нет'
        text += f'{lesson}: {note} \n'
    return text


def add_suffix(week, suffix):
    rweek = []
    for day in week:
        day += suffix
        rweek.append(day)
    return rweek


if __name__ == '__main__':
    days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб']
    days0 = add_suffix(days, ' ч')
    d = days0[1][3]
    print(d)
