class User:
    """
    there are statuses:
    reged_user,
    enter_lessons,
    day_ready,
    week_ready,
    reged,
    add_homework
    """

    def __init__(self, chat_id, group_name):
        self.chat_id = chat_id
        self.status = 'reged_user'
        self.group_name = group_name.lower() # use Upper
        self.curent_reg_day = 0
        self.days = {}
        self.lessons = {}
        self.days_list = []
        self.week_list = []
        self.curent_reg_week = 0
        self.lessons_list = []
        self.quantity_weaks = 1

    def day_ready_status(self):
        self.status = 'day_ready'

    def set_quantity_weaks(self,q):
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
        self.curent_reg_day = 0
        self.days = {}
        self.lessons = {}

    def enter_lessons_status(self):
        self.status = 'enter_lessons'
# methods for reged users
    def add_homework_status(self):
        self.status = 'add_homework'

    def add_homework(self, lesson, week, homework):
        """
        takes week "0,1" ;
        lesson;
        homework
        and add homework to next day that have this lesson.
        :returns False if there is not this lesson or not correct status:
        """
        if lesson in self.lessons_list and self.status == 'add_homework':
            for day in self.week_list[week].values():
                if lesson in day:
                    if not day[lesson]:
                        day[lesson] = homework
                        self.status = 'reged'
                        return
        else:
            self.status = 'reged'
            return False

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


def check_user(user_id):
    if user_id not in list(users.keys()):
        return False
    else:
        return


def registration(user_id, reg_info= None):
    """

    :param user_id:
    :param reg_info:
    :param group:
    :return:
    """
    try:
        reg_info= reg_info.lower()
    except AttributeError:
        pass
    answer = ''
    for user in list(users.values()):
        if user.group_name == reg_info and user.status == ('reg' or 'add_homework'):
            users[user_id] = user

    if user_id not in list(users.keys()):
        users[user_id] = User(user_id, reg_info)
        answer = 'Выбереите дни'
        # send request to chose days
    elif users[user_id].status == 'reged_user':
        # chose days
        if not reg_info == 'done':
            users[user_id].add_day(reg_info)
            answer = 'Выбереите дни'
        else:
            users[user_id].enter_lessons_status()
            answer = f'Добавьте первую пару на {users[user_id].get_current_reg_day()} (совет: ' \
                     f'добавляйте пары по которым могут выдать задание) '
            # send request to fill lessons
    elif users[user_id].status == 'enter_lessons':
        if not reg_info == 'done':
            users[user_id].add_lessons(reg_info)
            answer = 'Добавьте пару'
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
            print(f'знаменатель, {users[user_id].get_current_reg_day()}, введите первую пару')
        users[user_id].compile_week()

        print(users[user_id].week_list)
    print('log '+ users[user_id].status)
    return answer

def chating(user_id):
    pass


if __name__ == '__main__':
    i = 123
    while True:
        print(registration(i,reg_info=input('reg_info: ')))




