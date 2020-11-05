from data_class import User, reged_users
from keyboards import start_keyboard, days_keyboard, ready_keyboard, add_week_keyboard,\
    create_check_homework_keyboard, create_groups_keyboard, create_lessons_keyboard, create_choose_day_keyboard
import time_processes
import save_get_data
try:
    users = save_get_data.load_users()
except Exception:
    users = {}


def begining():
    groups = []
    for user in list(users.values()):
        if user.group_name not in groups:
            groups.append(user.group_name)
    keyboard = create_groups_keyboard(groups)
    return keyboard


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
    for user in list(users.values()):
        if user.group_name == reg_info and user.status == ('reg' or 'add_homework'):
            users[user_id] = user
            save_get_data.save_users(users)
            reged_users.append(user_id)

    if user_id not in list(users.keys()) and reg_info == 'добавить группу':
        answer = 'Введи свою группу'
        keyboard = None
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
            if users[user_id].status == 'week_ready' and users[user_id].quantity_weaks == 1:
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

        print(users[user_id].week_list)
    try:
        print('log ' + users[user_id].status)
    except KeyError:
        print('log user aren t have class')
    return [answer, keyboard]


def fill_homework(user_id, message):  # add keyboards
    user = users[user_id]
    message = message.lower()

    if message == 'добавить дз' and user.status == 'reged':
        user.add_homework_chose_lesson_status()
        return ['выберите предмет', create_lessons_keyboard(user.lessons_list)]
    elif user.status == 'add_homework_chose_lesson':
        user.homework.append(message)
        user.add_homework_chose_day_status()
        return 'выберите день'
    elif user.status == 'add_homework_chose_day':
        user.homework.append(message)
        user.add_homework_status()
        return 'Отправте дз'
    elif user.status == 'add_homework':
        user.homework.append(message)
        if not user.add_homework():
            return 'ошибка добавления'
        else:
            return 'задание отправлено'
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

    if message == 'узнать дз':
        tomorrow = time_processes.next_day_info()
        answer = user.get_homework_in_day(tomorrow[0], tomorrow[1])   # fixme need to parse
        if not answer:
            answer = 'У меня две новости: хорошая и плохая. \nХорошая: заданий нет \nПлохая: их могли забыть добавить'
        keyboard = create_check_homework_keyboard(user.days_list)
        user.check_homework_status()
        return [answer, keyboard]

    elif message == 'готово' and user.status == 'check_homework':
        answer = 'удачи'
        user.reged_status()
        keyboard = start_keyboard
        return [answer, keyboard]

    elif user.status == 'check_homework' and message[1] in user.lessons_list:
        answer = user.get_homework_in_day(message[0], message[1])         # need to parse answer
        keyboard = start_keyboard
        user.reged_status()
        return [answer, keyboard]

    elif user.status == 'check_homework' and message == 'выбрать предмет':
        user.check_homework_for_lesson_status()
        keyboard = create_lessons_keyboard(user.lessons_list)
        answer = 'выберите предмет'
        return [answer, keyboard]
    elif user.status == 'check_homework_for_lesson' and message in user.lessons_list:
        answer = user.get_current_homework(message)    # need to parse answer
        user.reged_status()
        keyboard = start_keyboard
        return [answer, keyboard]
    else:
        pass


def chating(user_id, message):
    if user_id not in reged_users:
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