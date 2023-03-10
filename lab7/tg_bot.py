import telebot
import psycopg2
import datetime
from telebot import types
from datetime import date

conn = psycopg2.connect(database="timestable_db",
                        user="postgres",
                        password="password",
                        host="localhost",
                        port="5433")
cursor = conn.cursor()
psql_select_timetable1 = "select day, string_agg(table_column, '\n\n') as table_row from (select day, timetable_week1.subject ||' | '|| room_numb ||' | '|| start_time ||'-'|| finish_time ||' | '|| full_name as table_column from timetable_week1, teacher where teacher.subject = timetable_week1.subject order by start_time)timetable_week1 group by 1 order by case when day = 'Monday' then 1 when day = 'Tuesday' then 2 when day = 'Wednesday' then 3 when day = 'Thursday' then 4 else 5 end;"
psql_select_timetable2 = "select day, string_agg(table_column, '\n\n') as table_row from (select day, timetable_week2.subject ||' | '|| room_numb ||' | '|| start_time ||'-'|| finish_time ||' | '|| full_name as table_column from timetable_week2, teacher where teacher.subject = timetable_week2.subject order by start_time)timetable_week2 group by 1 order by case when day = 'Monday' then 1 when day = 'Tuesday' then 2 when day = 'Wednesday' then 3 when day = 'Thursday' then 4 else 5 end;"


today = date.today()
num = int(today.isocalendar().week)
if (num % 2) == 0:
   this_week = "timetable_week2"
else:
   this_week = "timetable_week1"

if this_week == "timetable_week2":
    show_this_week = psql_select_timetable2
    show_next_week = psql_select_timetable1
else:
    show_this_week = psql_select_timetable1
    show_next_week = psql_select_timetable2

# store tgbot token
token = '6125194933:AAG-3e9VZQ59M5rNchFQ8ueAOOsVBjJ8Os4'
bot = telebot.TeleBot(token)


# decorator for /start
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row('/mtuci')
    keyboard.row('/week')
    keyboard.row('/this_week', '/next_week')
    keyboard.row('monday')
    keyboard.row('tuesday')
    keyboard.row('wednesday')
    keyboard.row('thursday')
    keyboard.row('friday')
    bot.send_message(message.chat.id,
                     'Hello! Do you want to know the newest MTUCI information? See /help for a list of commands',
                     reply_markup=keyboard)


# decorator for /help
@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'I can show you your timetable if you send me the day of the week. \nYou can control me by sending these commands: \n/mtuci - link to official mtuci website\n/week - tells you which timetable week it is\n/this_week - shows you the timetable for this week\n/next_week - shows you the timetable for next week')


# decorator for /mtuci
@bot.message_handler(commands=['mtuci'])
def start_message(message):
    bot.send_message(message.chat.id, 'You should check out - https://mtuci.ru/')


# decorator for /week
@bot.message_handler(commands=['week'])
def start_message(message):
    if this_week == 'timetable_week1':
        bot.send_message(message.chat.id, 'The week is odd')
    else:
        bot.send_message(message.chat.id, 'The week is even')


# decorator for this week
@bot.message_handler(commands=['this_week'])
def start_message(message):
    cursor.execute(show_this_week)
    tb1_records = cursor.fetchall()
    for row in tb1_records:
        w1_display = '{}\n___________________\n{} \n___________________'.format(row[0], row[1])
        bot.send_message(message.chat.id, w1_display)


# decorator for next week
@bot.message_handler(commands=['next_week'])
def start_message(message):
    cursor.execute(show_next_week)
    tb2_records = cursor.fetchall()
    for row in tb2_records:
        w2_display = '{}\n___________________\n{} \n___________________'.format(row[0], row[1])
        bot.send_message(message.chat.id, w2_display)


# decorator for monday
@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == 'monday':
        cursor.execute(
            "select day, string_agg(table_column, '\n\n') as table_row from (select day, {}.subject ||' | '|| room_numb ||' | '|| start_time ||'-'|| finish_time ||' | '|| full_name as table_column from {}, teacher where day ='Monday' and teacher.subject = {}.subject order by start_time) {} group by 1;".format(
                this_week, this_week, this_week, this_week))
        tb1_records = cursor.fetchall()
        for row in tb1_records:
            m1_display = '{}\n___________________\n{} \n___________________'.format(row[0], row[1])
            bot.send_message(message.chat.id, m1_display)
    elif message.text.lower() == 'tuesday':
        cursor.execute(
            "select day, string_agg(table_column, '\n\n') as table_row from (select day, {}.subject ||' | '|| room_numb ||' | '|| start_time ||'-'|| finish_time ||' | '|| full_name as table_column from {}, teacher where day ='Tuesday' and teacher.subject = {}.subject order by start_time) {} group by 1;".format(
                this_week, this_week, this_week, this_week))
        tb1_records = cursor.fetchall()
        for row in tb1_records:
            m1_display = '{}\n___________________\n{} \n___________________'.format(row[0], row[1])
            bot.send_message(message.chat.id, m1_display)
    elif message.text.lower() == 'wednesday':
        cursor.execute(
            "select day, string_agg(table_column, '\n\n') as table_row from (select day, {}.subject ||' | '|| room_numb ||' | '|| start_time ||'-'|| finish_time ||' | '|| full_name as table_column from {}, teacher where day ='Wednesday' and teacher.subject = {}.subject order by start_time) {} group by 1;".format(
                this_week, this_week, this_week, this_week))
        tb1_records = cursor.fetchall()
        for row in tb1_records:
            m1_display = '{}\n___________________\n{} \n___________________'.format(row[0], row[1])
            bot.send_message(message.chat.id, m1_display)
    elif message.text.lower() == 'thursday':
        cursor.execute(
            "select day, string_agg(table_column, '\n\n') as table_row from (select day, {}.subject ||' | '|| room_numb ||' | '|| start_time ||'-'|| finish_time ||' | '|| full_name as table_column from {}, teacher where day ='Thursday' and teacher.subject = {}.subject order by start_time) {} group by 1;".format(
                this_week, this_week, this_week, this_week))
        tb1_records = cursor.fetchall()
        for row in tb1_records:
            m1_display = '{}\n___________________\n{} \n___________________'.format(row[0], row[1])
            bot.send_message(message.chat.id, m1_display)
    elif message.text.lower() == 'friday':
        cursor.execute(
            "select day, string_agg(table_column, '\n\n') as table_row from (select day, {}.subject ||' | '|| room_numb ||' | '|| start_time ||'-'|| finish_time ||' | '|| full_name as table_column from {}, teacher where day ='Friday' and teacher.subject = {}.subject order by start_time) {} group by 1;".format(
                this_week, this_week, this_week, this_week))
        tb1_records = cursor.fetchall()
        for row in tb1_records:
            m1_display = '{}\n___________________\n{} \n___________________'.format(row[0], row[1])
            bot.send_message(message.chat.id, m1_display)
    elif message.text.lower() != '':
        bot.send_message(message.chat.id,
                         'Sorry, my master did not program me to deal with such complicated requests. Please respect me even with my lack of functionality <3')


bot.polling()
