


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
        if self.quantity_weaks == 1:
            week = 0
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


reged_users = []

