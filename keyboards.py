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
    button_tool(lessons_keyboard, lessons)
    return lessons_keyboard


def create_choose_day_keyboard(days: list):
    check_lessons_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_tool(check_lessons_keyboard, days)
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
    check_hmwk_keyboard = button_tool(check_hmwk_keyboard,days)
    check_hmwk_keyboard.add('Выбрать предмет')
    return check_hmwk_keyboard


def button_tool(keyboard, buttons_text):

    if len(buttons_text) == 10:
        keyboard.row(buttons_text[0], buttons_text[1], buttons_text[2], buttons_text[3], buttons_text[4],
                     buttons_text[5], buttons_text[6], buttons_text[7], buttons_text[8], buttons_text[9])
    if len(buttons_text) == 9:
        keyboard.row(buttons_text[0], buttons_text[1], buttons_text[2], buttons_text[3], buttons_text[4],
                     buttons_text[5], buttons_text[6], buttons_text[7], buttons_text[8])
    elif len(buttons_text) == 8:
        keyboard.row(buttons_text[0], buttons_text[1], buttons_text[2], buttons_text[3], buttons_text[4],
                     buttons_text[5], buttons_text[6], buttons_text[7])
    elif len(buttons_text) == 7:
        keyboard.row(buttons_text[0], buttons_text[1], buttons_text[2], buttons_text[3], buttons_text[4],
                     buttons_text[5], buttons_text[6])
    elif len(buttons_text) == 6:
        keyboard.row(buttons_text[0], buttons_text[1], buttons_text[2], buttons_text[3], buttons_text[4],
                     buttons_text[5])
    elif len(buttons_text) == 5:
        keyboard.row(buttons_text[0], buttons_text[1], buttons_text[2], buttons_text[3], buttons_text[4])
    elif len(buttons_text) == 4:
        keyboard.row(buttons_text[0], buttons_text[1], buttons_text[2], buttons_text[3])
    elif len(buttons_text) == 3:
        keyboard.row(buttons_text[0], buttons_text[1], buttons_text[2])
    elif len(buttons_text) == 2:
        keyboard.row(buttons_text[0], buttons_text[1])
    elif len(buttons_text) == 1:
        keyboard.row(buttons_text[0])
    else:
        for button in buttons_text:
            keyboard.row(button)

    return keyboard



if __name__ == '__main__':
    create_check_homework_keyboard(['пн', 'вт', 'ср', 'чт', 'пт', 'сб'])