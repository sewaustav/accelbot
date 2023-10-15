import config
import logging
from keyboard import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Command, Text
from aiogram import Bot, Dispatcher, executor, types
import psycopg2
from config import *


data = []
data_dump = []
connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

connection.autocommit = True

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    with connection.cursor() as cursor:
        postgres_insert_query =""" INSERT INTO users (user_id, user_name, user_surname, username)
                                           VALUES (%s,%s,%s,%s)"""
        record_to_insert = (user_id, user_name, user_surname, username)
        cursor.execute(postgres_insert_query, record_to_insert)

def db_table(user_id: int, nickname: str, age: int, citizenship: str, growth: int, weight: int, foot: str, club: str, contarct: bool, role: str, history: str, statistic: str, test: str, video: str, contact: str):
    with connection.cursor() as cursor:
        postgres_insert_query =""" INSERT INTO data (user_id, username, age, citizenship, growth, weight, foot, club, contract, role, history, statistic, test, video, contact)
                                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (user_id, nickname, age, citizenship, growth, weight, foot, club, contarct, role, history, statistic, test, video, contact)
        cursor.execute(postgres_insert_query, record_to_insert)

def dump_db(user_n):
    with connection.cursor() as cursor:
        postgresql_select_query = "SELECT * FROM data WHERE username = %s"
        cursor.execute(postgresql_select_query, (user_n,))
        result_n = cursor.fetchall()
        return result_n

def dump_by_id(user_i):
    with connection.cursor() as cursor:
        postgresql_select_query = "SELECT * FROM data WHERE id = %s"
        cursor.execute(postgresql_select_query, (user_i,))
        result_i = cursor.fetchall()
        return result_i

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKENN)
dp = Dispatcher(bot)

@dp.message_handler(commands = ["start"])
async def privet(message: types.Message):
    await message.answer("Привет! 👋")
    await message.answer("/go - начать заполнение\n /help - помощь \n/clear - начать запонение заново \n/del - удалить последнее введенное поле \n/hp - помощь по заполнению данных")


@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    await message.answer(f"Нужна помощь? \n/go - начать заполнение \n/clear - начать запонение заново \n/del - удалить последнее введенное поле \n/hp - помощь по заполнению данных" )

@dp.message_handler(commands=["go"])
async def go(message: types.Message):
    if len(data) == 0:
        await message.answer("Тогда начнем", reply_markup=button)

        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username


        db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)
        await bot.send_message(-703593824, f"{us_id}, {us_name}, {us_sname}, {username}")
    else:
        await message.answer("Извините, но с ботом уже работает человек. Попробуйте снова через 10 минут. Если есть вопросы, то пишите админу.")

@dp.message_handler(commands=["dumpadminall"])
async def dump_all(message: types.Message):
    print("data")
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM data"""
        )
        data_from_db = cursor.fetchall()
        for row in data_from_db:
            await message.answer(f"{row}")

@dp.message_handler(commands=["dumpadminnick"])
async def dump_nick(message: types.Message):
    data_dump.append("1")
    await message.answer("Введите ник")

@dp.message_handler(commands=["dumpadminid"])
async def dump_id(message: types.Message):
    data_dump.append("2")
    await message.answer("Введите id")


@dp.message_handler(commands=["OK"])
async def nick_name(message: types.Message):
    await message.answer("Поехали!", reply_markup=ReplyKeyboardRemove())
    await message.answer("Введи свой ник")

@dp.message_handler(Text(equals=["ВСЁ"]))
async def f_finish(message: types.Message):
    await message.answer("Ok", reply_markup=ReplyKeyboardRemove())
    await message.answer("Завершить?", reply_markup=finish)

@dp.message_handler(Text(equals=["Завершить"]))
async def oo(message: types.Message):
    await message.answer("Ваша анкета готовится к отправке!", reply_markup=ReplyKeyboardRemove())

    if data[7] == "Да":
        data[7] = True
    elif data[7] == "Нет":
        data[7] = False
    #await message.answer(f"{data}")
    if len(data) == 14:

        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username

        print(data)

        try:
            db_table(us_id, data[0], int(data[1]), data[2], int(data[3]), int(data[4]), data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13])
            await bot.send_message(-703593824, f"Бот закончил работу с {us_id}, {us_name}, {us_sname}, {username}")
            await message.answer("Ваша анкета отправлена модераторам!")
        except:
            await message.answer("Некорректно введены данные. Введите текст 'Начать заново'.")

    else:
        await message.answer("Неполные данные. Введите команду /go.")

    data.clear()

@dp.message_handler(Text(equals=["Начать заново"]))
async def f_restart(message: types.Message):
    data.clear()
    await message.answer(f"Ваши данные успешно сброшены{data}", reply_markup=ReplyKeyboardRemove())

@dp.message_handler(commands=["end"])
async def end(message: types.Message):
    data.clear()

    await message.answer("Вы завершили работу")

@dp.message_handler(commands=["del"])
async def dell(message: types.Message):
    try:
        data.pop()
    except:
        pass

    if len(data) == 0:
        await message.answer("Введите свой ник")
    elif len(data) == 1:
        await message.answer("Введите свой возраст")
    elif len(data) == 2:
        await message.answer("Гражданство")
    elif len(data) == 3:
        await message.answer("Укажите свой рост")
    elif len(data) == 4:
        await message.answer("Укажите свой вес")
    elif len(data) == 5:
        await message.answer("Ваша рабочая нога", reply_markup=foot)
    elif len(data) == 6:
        await message.answer("За какой клуб вы играете?")
    elif len(data) == 7:
        await message.answer("Есть ли у вас контракт?", reply_markup=contract)
    elif len(data) == 8:
        await message.answer("Введите свою позицию.", reply_markup=position)
    elif len(data) == 9:
        await message.answer("Напишите о себе")
    elif len(data) == 10:
        await message.answer("Ваша статистика:")
    elif len(data) == 11:
        await message.answer("Тесты:")
    elif len(data) == 12:
        await message.answer("Прикрепите ссылку на ваше видео")
    elif len(data) == 13:
        await message.answer("Вид связи:")
    elif len(data) == 14:
        await message.answer("Для завершения нажмите 👇👇👇", reply_markup=contact)

@dp.message_handler(commands=["hp"])
async def helper(message: types.Message):
    await message.answer("Напишите админу о вашей проблеме. Ссылка в описании.")

@dp.message_handler(commands=["clear"])
async def cl(message: types.Message):
    data.clear()
    await message.answer("Ваши данные успешно сброшены", reply_markup=ReplyKeyboardRemove())


@dp.message_handler()
async def i(message: types.Message):
    us_id = message.from_user.id

    print(*data)

    await message.answer("Запрос обработан!", reply_markup=ReplyKeyboardRemove())

    if data_dump == []:
        data.append(message.text)
        if len(data) == 0:
            await message.answer("Введите свой ник")
        elif len(data) == 1:
            await message.answer("Введите свой возраст")
        elif len(data) == 2:
            await message.answer("Гражданство")
        elif len(data) == 3:
            await message.answer("Укажите свой рост")
        elif len(data) == 4:
            await message.answer("Укажите свой вес")
        elif len(data) == 5:
            await message.answer("Ваша рабочая нога", reply_markup=foot)
        elif len(data) == 6:
            await message.answer("За какой клуб вы играете?")
        elif len(data) == 7:
            await message.answer("Есть ли у вас контракт?", reply_markup=contract)
        elif len(data) == 8:
            await message.answer("Введите свою позицию.", reply_markup=position)
        elif len(data) == 9:
            await message.answer("Напишите о себе")
        elif len(data) == 10:
            await message.answer("Ваша статистика:")
        elif len(data) == 11:
            await message.answer("Тесты:")
        elif len(data) == 12:
            await message.answer("Прикрепите ссылку на ваше видео")
        elif len(data) == 13:
            await message.answer("Вид связи:")
        elif len(data) == 14:
            await message.answer("Для завершения нажмите 👇👇👇", reply_markup=contact)
    else:
        if data_dump[0] == "1":
            mes = dump_db(message.text)
            await message.answer(f"{mes}")
        elif data_dump[0] == "2":
            mes = dump_by_id(int(message.text))
            await message.answer(f"{mes}")
        data_dump.clear()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)