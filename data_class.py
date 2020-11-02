from keyboards import start_keyboard, days_keyboard, ready_keyboard,\
    create_check_lessons_keyboard, create_groups_keyboard, create_lessons_keyboard
class User:
    """
    there are statuses:
    reged_user,
    enter_lessons,
    day_ready,
    week_ready,
    reged,

    add_homework
    add_homework_chose_lesson
    add_homework_chose_day

    check_homework_in_day
    check_homework_for_lesson
    check_homework

    """

    def __init__(self, chat_id, group_name):
        self.chat_id = chat_id
        self.status = 'reged_user'
        self.group_name = group_name.lower()  # use Upper
        self.curent_reg_day = 0
        self.days = {}
        self.lessons = {}
        self.days_list = []
        self.week_list = []
        self.curent_reg_week = 0
        self.lessons_list = []
        self.quantity_weaks = 1
        self.homework = []

    def day_ready_status(self):
        self.status = 'day_ready'

    def set_quantity_weaks(self, q):
        self.quantity_weaks = q

    def get_current_reg_day(self):
        return self.days_list[self.curent_reg_day]

    def add_day(self, day):
        if day not in self.days_list:
            self.days.update({day: None})
            self.days_list.append(day)

    def add_lessons(self, lesson):
        if lesson not in self.lessons.keys():
            self.lessons.update({lesson.lower(): None})
        if lesson not in self.lessons_list:
            self.lessons_list.append(lesson.lower())

    def compile_day(self):
        if self.status == 'day_ready':
            self.days[self.days_list[self.curent_reg_day]] = self.lessons
            self.lessons = {}
            self.curent_reg_day += 1
            if self.curent_reg_day == len(self.days_list):
                self.status = 'week_ready'
                self.curent_reg_day = 0
            else:
                self.status = 'enter_lessons'

    def compile_week(self):
        self.week_list.append(self.days)
        if len(self.week_list) < self.quantity_weaks:
            self.curent_reg_week += 1
            self.status = 'enter_lessons'
        else:
            self.status = 'reged'
            reged_users.append(self.chat_id)
        self.curent_reg_day = 0
        self.days = {}
        self.lessons = {}

    def enter_lessons_status(self):
        self.status = 'enter_lessons'

    def reged_status(self):
        self.status = 'reged'

    # methods for reged users
    def add_homework_chose_lesson_status(self):
        self.status = 'add_homework_chose_lesson'

    def add_homework_chose_day_status(self):
        self.status = 'add_homework_chose_day'

    def add_homework_status(self):
        self.status = 'add_homework'

    def add_homework(self):
        """
        takes week "0,1" ;
        lesson;
        homework
        and add homework to next day that have this lesson.
        :returns False if there is not this lesson or not correct status:
        """
        if self.homework[0] in self.lessons_list and self.status == 'add_homework':
            self.week_list[self.homework[0]][self.homework[1][0]][self.homework[1][1]] = self.homework[2]
        else:
            self.status = 'reged'
            return False

    def check_homework_status(self):
        self.status = 'check_homework'

    def check_homework_in_day_status(self):
        self.status = 'check_homework_in_day'

    def check_homework_for_lesson_status(self):
        self.status = 'check_homework_for_lesson'

    def get_all_homework(self):
        return self.week_list

    def get_homework_in_day(self, day, week):
        """
        :param day:
        :param week:
        :return False if there is no lessons:
        """
        if day in list(self.week_list[week].keys()):
            return self.week_list[week][day]
        else:
            return False

    def get_current_homework(self, lesson):
        """:returns dict {day: homework} """
        homework = {}
        for week in range(len(self.week_list)):
            for day in list(self.week_list[week].keys()):
                for less in list(self.week_list[week][day].keys()):
                    if less == lesson:
                        homework.update({day: self.week_list[week][day][less]})
        if homework:
            return homework
        else:
            return


users = {}
reged_users = []


def registration(user_id, reg_info=None):  # need to add keyboard in answer
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
    answer = ''
    for user in list(users.values()):
        if user.group_name == reg_info and user.status == ('reg' or 'add_homework'):
            users[user_id] = user

    if user_id not in list(users.keys()):
        users[user_id] = User(user_id, reg_info)
        answer = 'Выбереите дни'
        keyboard = days_keyboard
        # send request to chose days
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
            elif users[user_id].status == 'enter_lessons':
                answer = f'Добавьте пару на {users[user_id].get_current_reg_day()}'
            else:
                registration(user_id)
            # send request to fill lessons and current day
    elif users[user_id].status == 'week_ready':
        if reg_info == 'add_week':
            users[user_id].set_quantity_weaks(2)
            answer = f'знаменатель, {users[user_id].get_current_reg_day()}, введите первую пару'
        users[user_id].compile_week()

        print(users[user_id].week_list)
    print('log ' + users[user_id].status)
    return answer


def fill_homework(user_id, message):  # add keyboards
    user = users[user_id]
    message = message.lower()

    if message == 'добавить дз' and user.status == 'reged':
        user.add_homework_chose_lesson_status()
        return 'выберите предмет'
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
    :param message: gets buttons answer (if chose day -> message [week,day])
    :return:
    """
    user = users[user_id]
    try:
        message = message.lower()
    except AttributeError:
        pass

    if message == 'посмотреть дз':
        answer = user.get_homework_in_day(message[0], message[1])   # fix message[]
        user.check_homework_status()
        keyboard = create_check_lessons_keyboard(user.days_list)
        return answer
    elif message == 'готово' and user.status == 'check_homework':
        answer = 'удачи'
        user.reged_status()
        keyboard = start_keyboard
        return answer
    elif user.status == 'check_homework' and message[1] in user.lessons_list:
        answer = user.get_homework_in_day(message[0], message[1])         # need to parse answer
        user.reged_status()
        return answer
    elif user.status == 'check_homework' and message == 'выбрать предмет':
        user.check_homework_for_lesson_status()
        keyboard = create_lessons_keyboard(user.lessons_list)
        answer = 'выберите предмет'
        return answer
    elif user.status == 'check_homework_for_lesson' and message in user.lessons_list:
        answer = user.get_current_homework(message)    # need to parse answer
        user.reged_status()
        keyboard = start_keyboard
        return answer
    else:
        pass


def chating(user_id, message):
    if user_id not in reged_users:
        answer = registration(user_id, message)
    elif message == 'добавить дз' and users[user_id].status == 'reged' or \
            users[user_id].status.startswith('add_homework'):
        answer = fill_homework(user_id, message)
    elif message == 'посмотреть дз' and users[user_id].status == 'reged' or users[user_id].status.startswith('check_homework'):
        answer = check_homework(user_id, message)
    else:
        answer = 'не понял'

    return answer


if __name__ == '__main__':
    i = 123
    while True:
        print(chating(i, input('reg_info: ')))
