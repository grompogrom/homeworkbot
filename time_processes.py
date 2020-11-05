import time
import datetime


def check_time():
    row = time.ctime()
    t = time.strptime(row)
    timeinfo = {'mon': t.tm_mon, 'mday': t.tm_mday, 'wday': t.tm_wday, 'hour': t.tm_hour, 'min': t.tm_min}
    return timeinfo


def next_day_info(week_set=None):
    now = datetime.datetime.now()
    week_inf = now.isocalendar()
    next_wday = week_inf[2]
    if week_set:
        n_week = week_set
    else:
        n_week = week_inf[1] % 2
    days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
    wday = days[next_wday]
    return [n_week, wday]


if __name__ == '__main__':
    print(next_day_info())