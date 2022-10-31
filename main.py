import telebot
from telebot import types
from views import *
from settings import *
from db import *

bot = telebot.TeleBot(bot)


@bot.message_handler(commands=['start', 'go'])
def send_welcome(message):
    new_user(message, bot)

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    item1 = types.InlineKeyboardButton('Смотреть расписание', callback_data='output')
    item2 = types.InlineKeyboardButton('Создать расписание', callback_data='create')

    keyboard.add(item1, item2)

    bot.send_message(message.chat.id, 'Выбери:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['output'])
def callback_inline_one(call):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    group = all_group()

    for i in group:
        markup.add(types.KeyboardButton(i))

    msg = bot.send_message(call.message.chat.id, 'Выбери свою группу:', reply_markup=markup)

    bot.register_next_step_handler(msg, add_user_group, bot, types)


@bot.callback_query_handler(func=lambda call: call.data in ['create'])
def callback_inline_two(call):
    create_table(call.message)


"""# big батя всех объёмных изменений (и добавлений) в расписании
@bot.message_handler(commands=['create_table'])
def create_table(message):
    bot.send_message(message.chat.id, 'Отправь мне расписание по шаблону: ')
    bot.send_message(message.chat.id, 'Название группы / тип недели (где 1 - числитель/нечётная, 0 - \
знаменатель/четная) / номер дня недели (где 0 - понедельник, 6 - воскресенье) / какая пара по счету (начиная с 1) \
/ название предмета / номер аудитории / И.О.Фамилия преподавателя / тип занятия (лекция, семинар, занятие на стадионе)')
    bot.send_message(message.chat.id, 'Пример:\nИС2.2 / 1 / 0 / 1 / Архитектура ЭВМ / 213С / Ю.А.Половодов / Лек \n\
ИС2.2 / 1 / 0 / 2 / Операционные системы семейства Unix / 212С / Н.Р.Рудоман / Лек')
    bot.send_message(message.chat.id, 'Для группы ИС2.2 при числителе (нечётной неделе) расписание на день \
будет таким:')
    msg = bot.send_message(message.chat.id, 'Понедельник\n1. 8.00-9.20 Лек: Архитектура ЭВМ | Ю.А.Половодов 213С \n\
    2. 9.30-10.50 Лек: Операционные системы семейства Unix | Н.Р.Рудоман 213С')

    #bot.register_next_step_handler(msg, add_table)"""


# для единичного изменения
@bot.message_handler(commands=['add_table'])
def create_table(message):
    bot.send_message(message.chat.id, 'Отправь мне одну пару из расписания по шаблону: ')
    msg = bot.send_message(message.chat.id, 'Пример:\n\
ИС2.2 / 1 (нечёт. неделя) / 0 (понедельник) / 2 (номер пары) / Операционные системы семейства \
Unix / 212С (аудитория) / Н.Р.Рудоман / Лек')

    bot.register_next_step_handler(msg, add_table)


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "Я отказываюсь это делать.")


@bot.message_handler(commands=['table'])
def week_table_button(message):
    number_day = time.gmtime(message.date)[6]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if number_day == 5:
        markup.add(types.KeyboardButton('Сегодня'))
    elif number_day != 6:
        markup.add(types.KeyboardButton('Сегодня'))
        markup.add(types.KeyboardButton('Завтра'))
        for i in range(number_day + 2, 6):
            markup.add(types.KeyboardButton(string_days_week[i]))

    markup.add(types.KeyboardButton('Вся неделя'))

    bot.send_message(message.chat.id, 'Что показать?', reply_markup=markup)


# обработчик всего входящего текста
@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == 'Вся неделя':
        lessons = week_table(message)
        for i in lessons:
            bot.send_message(message.chat.id, i)
    elif message.text == 'Сегодня':
        lessons = day_table(string_days_week[time.gmtime(message.date)[6]], message)
        bot.send_message(message.chat.id, lessons)
    elif message.text == 'Завтра':
        lessons = day_table(string_days_week[time.gmtime(message.date)[6] + 1], message)
        bot.send_message(message.chat.id, lessons)
    elif message.text in string_days_week:
        lessons = day_table(message.text, message)
        bot.send_message(message.chat.id, lessons)
    else:
        help_command(message)


bot.infinity_polling()
