from telebot import types

remove_keyboard = types.ReplyKeyboardRemove()


start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

item_check = types.KeyboardButton('Узнать дз')
item_add = types.KeyboardButton('Добавить дз')
start_keyboard.add(item_check, item_add)

days_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
days_keyboard.add('пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'готово')

ready_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
ready_keyboard.add('готово')

add_week_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
add_week_keyboard.add('Добавить числитель', 'Нет')


def create_lessons_keyboard(lessons: list):
    lessons_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for lesson in lessons:
        button = types.KeyboardButton(lesson)
        lessons_keyboard.add(button)
    return lessons_keyboard


def create_choose_day_keyboard(days: list):
    check_lessons_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for day in days:
        check_lessons_keyboard.row(day)
    return check_lessons_keyboard


def create_groups_keyboard(groups):
    groups_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for group in groups:
        button = types.KeyboardButton(group)
        groups_keyboard.add(button)
    button = types.KeyboardButton('Добавить группу')
    groups_keyboard.add(button)
    return groups_keyboard


def create_check_homework_keyboard(days):
    check_hmwk_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    check_hmwk_keyboard.add('Суппер!')
    for day in days:
        check_hmwk_keyboard.add(day)
    check_hmwk_keyboard.add('Выбрать предмет')
    return check_hmwk_keyboard


if __name__ == '__main__':
    create_check_homework_keyboard(['пн', 'вт', 'ср', 'чт', 'пт', 'сб'])