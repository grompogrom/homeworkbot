from telebot import types

start_keybard = types.ReplyKeyboardMarkup()

item_check = types.KeyboardButton('Узнать дз')
item_add = types.KeyboardButton('Добавить дз')
start_keybard.add(item_check, item_add)

days_keyboard = types.ReplyKeyboardMarkup()
days_keyboard.add(['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'готово'])

ready_keyboard = types.ReplyKeyboardMarkup()
ready_keyboard.row('готово')
def create_lessons_keyboard(lessons: list):
    lessons_keyboard = types.ReplyKeyboardMarkup()
    for lesson in lessons:
        button = types.KeyboardButton(lesson)
        lessons_keyboard.add(button)
    return lessons_keyboard


def create_check_lessons_keyboard(days: list):
    chack_lessons_keyboard = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton('Thanks')
    chack_lessons_keyboard.add(button)
    chack_lessons_keyboard.row(days)
    button = types.KeyboardButton('Выбрать предмет')
    chack_lessons_keyboard.add(button)
    return chack_lessons_keyboard


def create_groups_keyboard(groups):
    groups_keyboard = types.ReplyKeyboardMarkup()
    for group in groups:
        button = types.KeyboardButton(group)
        groups_keyboard.add(button)
    button = types.KeyboardButton('Добавить группу')
    groups_keyboard.add(button)
    return groups_keyboard
