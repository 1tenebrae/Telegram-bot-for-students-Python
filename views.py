from db import *
import calendar
import time

string_days_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


# получение расписания на день
def day_table(day, message):

    a1 = str(get_type_week(message))

    """ for tests
    a3 = 1"""

    data_day = f"""
      SELECT group.name, id_time, start, end, title, teacher.name, number_class, type
      FROM `db_bot`.`SubjectTable`    
      INNER JOIN `db_bot`.`group` ON group.id = SubjectTable.id_group
      INNER JOIN `db_bot`.`lesson_time` ON SubjectTable.id_time = lesson_time.id
      INNER JOIN `db_bot`.`subject` ON SubjectTable.id_subject = subject.id
      INNER JOIN `db_bot`.`teacher` ON SubjectTable.id_teacher = teacher.id
      INNER JOIN `db_bot`.`type_lesson` ON SubjectTable.id_lesson = type_lesson.id
      INNER JOIN `db_bot`.`auditorium` ON SubjectTable.id_auditorium = auditorium.id 
      WHERE SubjectTable.day_week = '{str(string_days_week.index(day))}' 
      AND SubjectTable.id_group = '{get_id_group(message.chat.id)}'
      AND SubjectTable.type_week = '{a1}' 
    """

    data = execute_read_query(connection, data_day)

    day = [day]
    for pair in data:
        result_string = f'{str(pair[1])}. {int_to_time(pair[2])}-{int_to_time(pair[3])} {pair[7]}: {pair[4]} \
| {pair[5]} {pair[6]}'
        day.append(result_string)

    return '\n'.join(day)


# перевод времени из 800 к виду 8.00
def int_to_time(int_time):
    gg = int_time / 100.0
    gg_time = str('%.2f' % gg)
    return gg_time


# Возвращает массив с расписанием по дням
def week_table(message):
    week = []
    for i in range(0, 7):
        if i != 6:
            day = day_table(string_days_week[i], message)
            week.append(day)
    return week


# Бессовестно украла из интернета. Получает дату, возвращает номер недели
def get_week_num(day: int, month: int, year: int):
    calendar_ = calendar.TextCalendar(calendar.MONDAY)
    lines = calendar_.formatmonth(year, month).split('\n')
    days_by_week = [week.lstrip().split() for week in lines[2:]]
    str_day = str(day)
    for index, week in enumerate(days_by_week):
        if str_day in week:
            return index + 1


def get_type_week(message):
    struct_time = time.gmtime(message.date)
    number_week = get_week_num(struct_time[2], struct_time[1], struct_time[0])

    return number_week % 2


# Вид: 4 / 0 / 0 / 1 / 3 / 3 / 3 / 3
# Добавляет одну строку в расписание
def add_one_lesson(id_group, type_week, day_week,  id_time, id_subject, id_auditorium, id_teacher, id_lesson):
    def_data = [id_group, type_week, day_week,  id_time, id_subject, id_auditorium, id_teacher, id_lesson]

    query_data_subjecttable = f"""
    SELECT id_group, type_week, day_week,  id_time, id_subject, id_auditorium, id_teacher, id_lesson
    FROM `db_bot`.`SubjectTable`
    WHERE SubjectTable.id_group = '{id_group}' 
    AND SubjectTable.type_week = '{type_week}'
    AND SubjectTable.day_week = '{day_week}'
    AND SubjectTable.id_time = '{id_time}'
    """

    data = execute_read_query(connection, query_data_subjecttable)

    if not len(data):
        query_add_lesson = f"""
        INSERT INTO
        `db_bot`.`SubjectTable`
        (id_group, type_week, day_week,  id_time, id_subject, id_auditorium, id_teacher, id_lesson)
        VALUES
        ({id_group}, {type_week}, {day_week}, {id_time}, {id_subject}, {id_auditorium}, {id_teacher}, {id_lesson})
        """
        execute_query(connection, query_add_lesson)

        #print('Добавлена строка в расписание ', def_data)

    elif data != def_data:
        query_update_lesson = f"""
        UPDATE
        `db_bot`.`SubjectTable`
        SET
        SubjectTable.id_subject = '{id_subject}',
        SubjectTable.id_auditorium = '{id_auditorium}',
        SubjectTable.id_teacher = '{id_teacher}',
        SubjectTable.id_lesson = '{id_lesson}'
    """
        execute_query(connection, query_update_lesson)
        #print('Обновлена строка в расписании ', def_data)


def add_table(message):
    msg = message.text.split(' / ')

    id_group = transform_name_group(get_id_user(message.chat.id), msg[0])

    if id_group is not None:
        id_subject = transform_name_subject(msg[4])
        id_auditorium = transform_name_auditorium(msg[5])
        id_teacher = transform_name_teacher(msg[6])
        id_lesson = transform_name_lesson(msg[7])
        add_one_lesson(id_group, msg[1], msg[2], msg[3], id_subject, id_auditorium, id_teacher, id_lesson)
    else:
        print('Нет прав на изменение этой группы')
