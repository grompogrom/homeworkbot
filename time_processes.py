import datetime
import pytz


def next_day_info(week_set=None):
    tz1 = pytz.timezone('Etc/GMT+3')
    now = datetime.datetime.now(tz=tz1)
    week_inf = now.isocalendar()
    next_wday = week_inf[2] % 7
    if week_set:
        n_week = week_set
    else:
        n_week = week_inf[1] % 2
    days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
    wday = days[next_wday]
    return [n_week, wday]


if __name__ == '__main__':
    print(next_day_info())