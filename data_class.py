import save_get_data


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
        self.group_name = group_name.upper()  # use Upper
        if self.group_name in list(groups.keys()):
            self.status = 'reged'
            self.week_list = groups[self.group_name]['week_list']
            self.days_list = groups[self.group_name]['days_list']
            self.lessons_list = groups[self.group_name]['lessons_list']
            self.quantity_weeks = groups[self.group_name]['quantity_weeks']
        else:
            groups[self.group_name] = {}
            self.status = 'reged_user'
            self.days_list = []
            self.week_list = []
            self.lessons_list = []
            self.quantity_weeks = 1
        self.curent_reg_day = 0
        self.days = {}
        self.lessons = {}
        self.curent_reg_week = 0
        self.homework = {'lesson': None, 'day': None}

    def day_ready_status(self):
        self.status = 'day_ready'

    def set_quantity_weaks(self, q):
        self.quantity_weeks = q

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

    def update_global_data(self):
        reged_users.append(self.chat_id)
        save_get_data.save_reged(reged_users)

        groups[self.group_name]['week_list'] = self.week_list
        groups[self.group_name]['days_list'] = self.days_list
        groups[self.group_name]['lessons_list'] = self.lessons_list
        groups[self.group_name]['quantity_weeks'] = self.quantity_weeks
        save_get_data.save_groups(groups)

    def compile_week(self):
        self.week_list.append(self.days)
        if len(self.week_list) < self.quantity_weeks:
            self.curent_reg_week += 1
            self.status = 'enter_lessons'
        else:
            self.status = 'reged'
            self.update_global_data()

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

    def find_day_with_lesson(self, lesson):
        days = []
        for week in self.week_list:
            for day in list(week.keys()):
                if lesson in week[day].keys():
                    days.append(day)
        return days

    def add_homework_lesson(self, lesson):
        if lesson in self.lessons_list:
            self.homework['lesson'] = lesson
            self.status = 'add_homework_chose_day'

    def add_homework_day(self, day):
        if day in self.find_day_with_lesson(self.homework['lesson']):
            self.homework['day'] = day
            self.status = 'add_homework'

    def add_homework(self, note):  # fixme add supporting 2 weeks
        """

        """
        if self.status == 'add_homework':
            self.week_list[0][self.homework['day']][self.homework['lesson']] = note
            self.update_global_data()
            self.status = 'reged'
        self.homework = {}

    def check_homework_status(self):
        self.status = 'check_homework'

    def check_homework_in_day_status(self):
        self.status = 'check_homework_in_day'

    def check_homework_for_lesson_status(self):
        self.status = 'check_homework_for_lesson'

    def get_all_homework(self):
        return self.week_list

    def get_homework_in_day(self, week, day):
        """
        :param day:
        :param week:
        :return False if there is no lessons:
        """
        if self.quantity_weeks == 1:
            week = 0
        if day in list(self.week_list[week].keys()):
            return self.week_list[week][day]
        else:
            return False

    def get_current_homework(self, lesson):
        """:returns dict {day: homework} """
        homework = {}
        for week in self.week_list:
            print(week)
            for day in list(week.keys()):
                for less in list(week[day].keys()):
                    if less == lesson:
                        homework.update({day: week[day][less]})
        return homework


try:
    reged_users = save_get_data.load_reged()
except Exception:
    reged_users = []

try:
    groups = save_get_data.load_groups()
except Exception:
    groups = {}
