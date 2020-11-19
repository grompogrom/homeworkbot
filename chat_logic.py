from data_class import User, reged_users, groups
from keyboards import start_keyboard, days_keyboard, ready_keyboard, add_week_keyboard, remove_keyboard,\
    create_check_homework_keyboard, create_groups_keyboard, create_lessons_keyboard, create_choose_day_keyboard
import time_processes
import save_get_data
import tools
try:
    users = save_get_data.load_users()
except Exception:
    users = {}


def begining(user_id):
    if user_id not in list(users.keys()):
        keyboard = create_groups_keyboard(list(groups.keys()))
        answer = 'Доров, выбери свою группу'
        return [answer, keyboard]
    else:
        answer = 'Нормально же общались. Что ты начинаешь'
        return [answer, start_keyboard]


def registration(user_id, reg_info=None):
    """
    Takes unreged user
    :param user_id:
    :param reg_info:
    :return:
    """
    try:
        reg_info = reg_info.lower()
    except AttributeError:
        pass

    answer = None
    keyboard = None

    if reg_info.upper() in list(groups.keys()) and user_id not in list(users.keys()):
        users[user_id] = User(user_id, reg_info)
        save_get_data.save_users(users)
        reged_users.append(user_id)
        save_get_data.save_reged(reged_users)
        answer = 'Да да, припоминаю. Славная группа!'
        keyboard = start_keyboard
    elif user_id not in list(users.keys()) and reg_info == 'добавить группу':
        answer = 'Введи свою группу'
        keyboard = remove_keyboard
    elif user_id not in list(users.keys()):
        users[user_id] = User(user_id, reg_info)
        save_get_data.save_users(users)
        answer = 'Выбереите дни'
        keyboard = days_keyboard
    elif users[user_id].status == 'reged_user':
        # chose days
        if not reg_info == 'готово':
            users[user_id].add_day(reg_info)
            answer = 'Выбереите дни'
            keyboard = days_keyboard
        else:
            users[user_id].enter_lessons_status()
            answer = f'Добавьте первую пару на {users[user_id].get_current_reg_day()} (совет: ' \
                     f'добавляйте пары по которым могут выдать задание) '
            keyboard = ready_keyboard
            # send request to fill lessons
    elif users[user_id].status == 'enter_lessons':
        if not reg_info == 'готово':
            users[user_id].add_lessons(reg_info)
            answer = 'Добавьте пару'
            keyboard = ready_keyboard
            # send request to fill lessons and current day
        else:
            users[user_id].day_ready_status()
            users[user_id].compile_day()
            if users[user_id].status == 'week_ready' and users[user_id].quantity_weeks == 1:
                answer = 'Добавить числитель?'
                keyboard = add_week_keyboard
            elif users[user_id].status == 'enter_lessons':
                answer = f'Добавьте пару на {users[user_id].get_current_reg_day()}'
            else:
                answer = registration(user_id)
                keyboard = start_keyboard
    elif users[user_id].status == 'week_ready':
        if reg_info == 'добавить числитель':
            users[user_id].set_quantity_weaks(2)
            answer = f'знаменатель, {users[user_id].get_current_reg_day()}, введите первую пару'
            keyboard = ready_keyboard
        else:
            answer = 'рассписание составленно )'
            keyboard = start_keyboard
        users[user_id].compile_week()
        save_get_data.save_users(users)

        print(users[user_id].week_list)
    try:
        print('log ' + users[user_id].status)
    except KeyError:
        print('log user aren t have class')
    return [answer, keyboard]


def fill_homework(user_id, message):  # add supporting weeks and protection
    user = users[user_id]
    message = message.lower()

    if message == 'добавить дз' and user.status == 'reged':
        user.add_homework_chose_lesson_status()
        return ['Выберите предмет', create_lessons_keyboard(user.lessons_list)]
    elif user.status == 'add_homework_chose_lesson':
        if user.add_homework_lesson(message):
            answer = 'Выберите день'
            keyboard = create_choose_day_keyboard(user.find_day_with_lesson(message))
        else:
            answer = 'Упс... Такого предмета нет'
            keyboard = create_lessons_keyboard(user.lessons_list)
        return [answer, keyboard]
    elif user.status == 'add_homework_chose_day':
        user.add_homework_day(message)
        answer = 'Введите задание'
        keyboard = remove_keyboard
        return [answer, keyboard]
    elif user.status == 'add_homework':
        user.add_homework(message)
        save_get_data.save_users(users)
        answer = 'Задание добавленно!'
        keyboard = start_keyboard
        return [answer, keyboard]
    else:
        pass


def check_homework(user_id, message):  # not tested
    """

    :param user_id:
    :param message:
    :return:
    """
    user = users[user_id]
    try:
        message = message.lower()
    except AttributeError:
        pass

    print(message, user.lessons_list)
    if message == 'узнать дз' and user.status == 'reged':
        tomorrow = time_processes.next_day_info()
        answer = user.get_homework_in_day(tomorrow[0], tomorrow[1])
        if answer:
            answer = tools.message_parser(answer)
        else:
            answer = 'У меня две новости: хорошая и плохая. \nХорошая: заданий на завтра нет \nПлохая: их могли ' \
                     'забыть добавить '
        keyboard = create_check_homework_keyboard(user.days_list, quantity=user.quantity_weeks)
        user.check_homework_status()
        return [answer, keyboard]

    elif message == 'суппер!' and user.status == 'check_homework':
        answer = 'удачи'
        user.reged_status()
        keyboard = start_keyboard
        return [answer, keyboard]

    elif user.status == 'check_homework' and message.startswith(tuple(user.days_list)):
        try:
            date = tools.to_week_day(message)
            day = date[1]
            week = date[0]
        except Exception:
            keyboard = create_check_homework_keyboard(user.days_list, quantity=user.quantity_weeks)
            return ['Упс... Такого дня нет)', keyboard]
        answer = user.get_homework_in_day(week, day)
        answer = tools.message_parser(answer).title()
        keyboard = start_keyboard
        user.reged_status()
        return [answer, keyboard]

    elif user.status == 'check_homework' and message == 'выбрать предмет':
        user.check_homework_for_lesson_status()
        keyboard = create_lessons_keyboard(user.lessons_list)
        answer = 'выберите предмет'
        return [answer, keyboard]
    elif user.status == 'check_homework_for_lesson' and message in user.lessons_list:
        answer = user.get_current_homework(message)
        answer = tools.message_parser(answer).title()
        user.reged_status()
        keyboard = start_keyboard
        return [answer, keyboard]
    else:
        keyboard = create_check_homework_keyboard(user.days_list, quantity=user.quantity_weeks)
        user.check_homework_status()
        return ['Упс...', keyboard]


def chating(user_id, message):
    print(message)
    try:
        print('chating', users[user_id].status)
    except Exception:
        print('chating Not reged_user')
    if user_id not in reged_users:
        print('registration')
        answer = registration(user_id, message)
    elif message == 'Добавить дз' and users[user_id].status == 'reged' or \
            users[user_id].status.startswith('add_homework'):
        answer = fill_homework(user_id, message)
    elif message == 'Узнать дз' and users[user_id].status == 'reged' or users[user_id].status.startswith('check_homework'):
        answer = check_homework(user_id, message)
    else:
        answer = ['не понял', start_keyboard]

    return answer


if __name__ == '__main__':
    i = 123
    while True:
        print(chating(i, input('reg_info: ')))