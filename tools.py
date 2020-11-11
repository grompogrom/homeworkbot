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


def to_week_day(rday):
    if rday.endswith('з'):
        week = 1
    else:
        week = 0
    day = rday[0:2]
    return week, day


def to_rday(week, day):
    if week == 0:
        suff = ' ч'
    elif week == 1:
        suff = ' з'
    else:
        suff = ''
    rday = day + suff
    return rday


if __name__ == '__main__':
    x = to_week_day('пн ч')
    y = to_week_day('вт з')
    print(x,y)
