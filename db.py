import mysql.connector
from mysql.connector import Error


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


connection = create_connection("localhost", "root", "root", "db_bot")


# для чтения из БД
def execute_read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


# для записи в БД
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# добавление нового пользователя в БД
def new_user(message, bot):

    bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name + '!')

    add_user = f"""
        INSERT INTO
         `db_bot`.`user` (username, chat)
        VALUES
        ('{message.from_user.username}', '{message.chat.id}')
    """

    execute_query(connection, add_user)


# получение из БД всех учебных групп в один список
def all_group():
    all_groups = """
       SELECT name
        FROM `db_bot`.`group`;
       """

    all_groups = execute_read_query(connection, all_groups)

    groups = [i[0] for i in all_groups]

    return groups


# Переписывает группу пользователю, в т.ч. из пустого значения
def add_user_group(message, bot, types):
    id_group = f"""
    SELECT id
    FROM `db_bot`.`group`
    WHERE group.name = '{message.text}'
    """

    id_group = execute_read_query(connection, id_group)

    id_group = id_group[0][0]

    new_group = f"""
    UPDATE
      `db_bot`.`user`
    SET
      id_group = '{id_group}'
    WHERE chat = '{message.chat.id}'
    """

    execute_query(connection, new_group)

    bot.send_message(message.chat.id, 'Теперь твоя группа: ' + message.text + '\nВведи /table \
для просмотра расписания', reply_markup=types.ReplyKeyboardRemove())


# по ID чата определяет id учебной группы пользователя
def get_id_group(id_chat):
    user_group = f"""
    SELECT id_group
    FROM `db_bot`.`user`
    WHERE user.chat = '{str(id_chat)}'
    """

    ray = execute_read_query(connection, user_group)

    result = str(ray[0][0])

    return result


# по id чата возвращает id пользователя в БД
def get_id_user(chat_id):
    query_id = f"""
    SELECT id
    FROM `db_bot`.`user`
    WHERE user.chat = '{str(chat_id)}'
    """

    aray = execute_read_query(connection, query_id)

    return int(aray[0][0])


# Просто запрос на данные из БД. Столбцы бд через зпт, имя таблицы, поле условия, чему равно условие.
def read_transformer(column_db, name_db, column_condition, condition):
    query = f"""
    SELECT {column_db}
    FROM `db_bot`.`{name_db}` 
    WHERE {column_condition} = \'{condition}\'
    """

    return execute_read_query(connection, query)


def write_transformer(name_db, column_db, value):
    query = f"""
        INSERT INTO
        `db_bot`.`{name_db}` ({column_db})
        VALUES
        ('{value}')
        """

    return execute_query(connection, query)


# получает группу в виде текста, делает проверку на доступ к группе, возвращает id группы в бд для вставки в осн таблицу
def transform_name_group(id_user, name_group):
    id_group = None
    query_read_groups = f"""
        SELECT group.id, group.name, group.id_head, user.id, user.chat
        FROM `db_bot`.`group` 
        INNER JOIN `db_bot`.`user` ON user.id = group.id_head
        WHERE group.name = '{name_group}'
        """

    data = execute_read_query(connection, query_read_groups)

    if not len(data):
        add_group_query = f"""
            INSERT INTO
             `db_bot`.`group` (name, id_head)
            VALUES
            ('{name_group}', {id_user})
            """
        execute_query(connection, add_group_query)
        data = read_transformer('id', 'group', 'group.name', name_group)
        id_group = data[0][0]
    elif data[0][2] == id_user:
        id_group = data[0][0]

    return id_group


def transform_name_subject(name_subject):
    write_transformer('subject', 'title', name_subject)
    data = read_transformer('id', 'subject', 'subject.title', name_subject)

    id_subject = data[0][0]

    return id_subject


def transform_name_auditorium(name_auditorium):
    write_transformer('auditorium', 'number_class', name_auditorium)
    data = read_transformer('id', 'auditorium', 'auditorium.number_class', name_auditorium)

    id_subject = data[0][0]

    return id_subject


def transform_name_teacher(name_teacher):
    write_transformer('teacher', 'name', name_teacher)
    data = read_transformer('id', 'teacher', 'teacher.name', name_teacher)

    id_teacher = data[0][0]

    return id_teacher


def transform_name_lesson(name_lesson):
    write_transformer('type_lesson', 'type', name_lesson)
    data = read_transformer('id', 'type_lesson', 'type_lesson.type', name_lesson)

    id_lesson = data[0][0]

    return id_lesson
