from aiogram import Dispatcher, types, Bot, F
from aiogram.filters import Command
import asyncio
import pandas as pd
import time
from email_sender import send_email

global buttons, admins, emails, price, avto, contacts, shops, chickens

users = {}


def updates_tables():
    global buttons, admins, emails,  price, avto, contacts, shops, chickens, time_out
    temp_v = ''
    buttons = {'price': '', 'avto': '', 'contacts': '', 'shops': '', 'chickens': ''}
    admins = []
    emails = []
    time_out = 0
    fi = open('config.txt', 'r')
    f = fi.read().split('\n')
    for i in f:
        if temp_v == '':
            temp_v = i
        elif temp_v == 'Files':
            if i == '':
                temp_v = i
            else:
                a, b = i.split()
                for j in buttons.keys():
                    if a == j:
                        buttons[j] = b
        elif temp_v == 'Admins':
            if i == '':
                temp_v = i
            else:
                admins.append(i)
        elif temp_v == 'Emails':
            if i == '':
                temp_v = i
            else:
                emails.append(i)
        elif temp_v == 'TimeOut':
            if i == '':
                temp_v = i
            else:
                time_out = i
    fi.close()

    df = pd.read_excel(buttons['price'], usecols=[0, 1, 2, 3], sheet_name=0, skiprows=0, header=0)
    price = df.values.tolist()
    df = pd.read_excel(buttons['avto'], usecols=[0, 1, 2], sheet_name=0, skiprows=0, header=0)
    avto = df.values.tolist()
    df = pd.read_excel(buttons['contacts'], usecols=[0, 1], sheet_name=0, skiprows=0, header=0)
    contacts = df.values.tolist()
    df = pd.read_excel(buttons['shops'], usecols=[0, 1, 2, 3], sheet_name=0, skiprows=0, header=0)
    shops = df.values.tolist()
    df = pd.read_excel(buttons['chickens'], usecols=[0, 1, 2], sheet_name=0, skiprows=0, header=0)
    chickens = df.values.tolist()


dp = Dispatcher()
updates_tables()


@dp.message(Command('start'))
async def start_cmd(message: types.Message) -> None:
    if not (str(message.from_user.id) in users.keys()):
        users[str(message.from_user.id)] = ['start', time.time()]
    if str(str(message.from_user.id)) in admins:
        await message.answer(f'Здравствуйте, {message.from_user.first_name}! \n\n'
                             f'Список команд для управления ботом:\n'
                             f'/start - начало диалога с ботом, перезапуск бота\n'
                             f'/help - помощь, список команд для управления ботом\n'
                             f'/menu - выбор категории вопроса\n'
                             f'/update - обновление таблиц и конфигурационного файла\n'
                             f'/view - просмотр всех сессий\n'
                             f'/reload - обновление всех сессий работы с ботом\n')
    else:
        await message.answer(
            f'Здравствуйте, {message.from_user.first_name}! \n'
            f'Для выбора подходящей категории вопроса нажмите /menu. \n'
            f'Для получения помощи нажмите /help.')
    users[str(message.from_user.id)][0] = 'start_cmd'
    users[str(message.from_user.id)][1] = time.time()


@dp.message(Command('help'))
async def help_cmd(message: types.Message) -> None:
    if str(message.from_user.id) in admins:
        await message.answer(f'Список команд для управления ботом:\n'
                             f'/start - начало диалога с ботом, перезапуск бота\n'
                             f'/help - помощь, список команд для управления ботом\n'
                             f'/menu - выбор категории вопроса\n'
                             f'/update - обновление таблиц и конфигурационного файла\n'
                             f'/view - просмотр всех сессий\n'
                             f'/reload - обновление всех сессий работы с ботом\n')
    else:
        await message.answer(f'Чтобы вызвать меню, напиши /menu\n'
                             f'Выберете раздел наиболее подходящий под ваш запрос\n'
                             f'Для подтверждения выбора, нажмите на соответствующую кнопку')
    users[str(message.from_user.id)][0] = 'help_cmd'
    users[str(message.from_user.id)][1] = time.time()


@dp.message(Command('update'))
async def update_cmd(message: types.Message) -> None:
    if str(str(message.from_user.id)) in admins:
        updates_tables()
        await message.answer('База данных обновлена')
    else:
        await message.answer('Отказано в доступе')
        #print(admins)
    users[str(message.from_user.id)][0] = 'update_cmd'
    users[str(message.from_user.id)][1] = time.time()


@dp.message(Command('menu'))
async def menu_cmd(message: types.Message) -> None:
    kb = [
        [types.KeyboardButton(text='Магазины'), types.KeyboardButton(text='Автолавка')],
        [types.KeyboardButton(text='Цена'), types.KeyboardButton(text='Цыплята'),
         types.KeyboardButton(text='Контакты')],
        [types.KeyboardButton(text='Претензии обслуживание')],
        [types.KeyboardButton(text='Претензии продукция')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Выберите подходящий пункт меню. \n', reply_markup=keyboard)
    users[str(message.from_user.id)][0] = 'menu_cmd'
    users[str(message.from_user.id)][1] = time.time()


@dp.message(Command('reload'))
async def reload_users_cmd(message: types.Message) -> None:
    if str(str(message.from_user.id)) in admins:
        del_users = []
        for i in users.keys():
            if (time.time() - users[i][1]) > int(time_out):
                if not (i in admins):
                    del_users.append(i)
        for i in del_users:
            users.pop(i)
        users[str(message.from_user.id)][0] = 'reload_users_cmd'
        users[str(message.from_user.id)][1] = time.time()
        await message.answer(f'Session was reloaded')
    else:
        await message.answer('Отказано в доступе')


@dp.message(Command('view'))
async def view_users_cmd(message: types.Message) -> None:
    if str(str(message.from_user.id)) in admins:
        for i in users.keys():
            await message.answer(f'{i} - {users[i][0]} - {(time.time() - users[i][1])}')
        users[str(message.from_user.id)][0] = 'view_users_cmd'
        users[str(message.from_user.id)][1] = time.time()
    else:
        await message.answer('Отказано в доступе')


#-----------------------------------------------ОБЫЧНЫЕ КНОПКИ-------------------------------------------


@dp.message(F.text.lower() == 'цена')
async def price_b(message: types.Message) -> None:
    await message.answer('Введите название интересующего товара')
    users[str(message.from_user.id)][0] = 'price'
    users[str(message.from_user.id)][1] = time.time()


@dp.message(F.text.lower() == 'магазины')
async def shops_b(message: types.Message) -> None:
    await message.answer('Введите адрес интересующего магазина')
    users[str(message.from_user.id)][0] = 'shops'
    users[str(message.from_user.id)][1] = time.time()


@dp.message(F.text.lower() == 'автолавка')
async def avtoshop_b(message: types.Message) -> None:
    await message.answer('Введите название интересующего населенного пунка')
    users[str(message.from_user.id)][0] = 'avtoshop'
    users[str(message.from_user.id)][1] = time.time()


@dp.message(F.text.lower() == 'цыплята')
async def chickens_b(message: types.Message) -> None:
    await message.answer('Введите интересующее название или город покупки')
    users[str(message.from_user.id)][0] = 'chickens'
    users[str(message.from_user.id)][1] = time.time()



@dp.message(F.text.lower() == 'контакты')
async def contacts_b(message: types.Message) -> None:
    await message.answer('Укажите должность представителя компании')
    users[str(message.from_user.id)][0] = 'contacts'
    users[str(message.from_user.id)][1] = time.time()


@dp.message(F.text.lower() == 'претензии обслуживание')
async def service_clims_b(message: types.Message) -> None:
    await message.answer('Опишите вашу претензию')
    users[str(message.from_user.id)][0] = 'service_clims'
    users[str(message.from_user.id)][1] = time.time()


@dp.message(F.text.lower() == 'претензии продукция')
async def product_clims_b(message: types.Message) -> None:
    await message.answer('Опишите вашу претензию')
    users[str(message.from_user.id)][0] = 'product_clims'
    users[str(message.from_user.id)][1] = time.time()


@dp.message()
async def other(message: types.Message) -> None:

    if users[str(message.from_user.id)][0] == 'product_clims':
        for i in emails:
            send_email('XXX@mail.ru', i, 'product_clims', message.text,
                       'smtp.mail.ru', 587, 'XXX@mail.ru', 'XXX')
        await message.answer('Претензия успешно отправлена!')
        users[str(message.from_user.id)][0] = 'clims'
    elif users[str(message.from_user.id)][0] == 'service_clims':
        for i in emails:
            send_email('XXX@mail.ru', i, 'service_clims', message.text,
                       'smtp.mail.ru', 587, 'XXX@mail.ru', 'XXX')
        await message.answer('Претензия успешно отправлена!')
        users[str(message.from_user.id)][0] = 'clims'
    elif users[str(message.from_user.id)][0] == 'avtoshop':
        f = 0
        find_flag = 0
        for i in range(len(avto)):
            if avto[i][0].lower().find(message.text.lower()) != -1:
                if f == 0:
                    await message.answer('Найдены следующие населенные пункты:')
                    f = 1
                await message.answer(f'{avto[i][0]} - {avto[i][1]} ')
                find_flag = 1
        if find_flag == 0:
            await message.answer('Не могу найти данный населенный пункт.')
            await message.answer(f'Попробуйте ввести другое название или выберите другой пункт меню, '
                                 f'для этого введите /menu.')
            users[str(message.from_user.id)][0] = 'avtoshop'
    elif users[str(message.from_user.id)][0] == 'shops':
        f = 0
        find_flag = 0
        for i in range(len(shops)):
            if shops[i][0].lower().find(message.text.lower()) != -1:
                if f == 0:
                    await message.answer('Найдены следующие магазины:')
                    f = 1
                await message.answer(f'{shops[i][0]}\nТел. {shops[i][1]}\n'
                                     f'Время работы: {shops[i][2]}\nЦеновая группа: {shops[i][3]}')
                find_flag = 1
        if find_flag == 0:
            await message.answer('Не могу найти данный магазин.')
            await message.answer(f'Попробуйте ввести другое название или выберите другой пункт меню, '
                                 f'для этого введите /menu.')
            users[str(message.from_user.id)][0] = 'shops'
    elif users[str(message.from_user.id)][0] == 'price':
        f = 0
        find_flag = 0
        for i in range(len(price)):
            if price[i][0].lower().find(message.text.lower()) != -1:
                if f == 0:
                    await message.answer('Найдены следующие товары:')
                    f = 1
                await message.answer(f'{price[i][0]}, {price[i][3]}\n'
                                     f'Цена в магазинах I категории: {price[i][1]}р.\n'
                                     f'Цена в магазинах II категории: {price[i][2]}р.')
                find_flag = 1
        if find_flag == 0:
            await message.answer('Не могу найти данный товар.')
            await message.answer(f'Попробуйте ввести другое название или выберите другой пункт меню, '
                                 f'для этого введите /menu.')
            users[str(message.from_user.id)][0] = 'price'
    elif users[str(message.from_user.id)][0] == 'chickens':
        f = 0
        find_flag = 0
        for i in range(len(chickens)):
            if ((chickens[i][0].lower().find(message.text.lower()) != -1) or
                    (chickens[i][1].lower().find(message.text.lower()) != -1)):
                if f == 0:
                    await message.answer('Найдены следующие варианты:')
                    f = 1
                kb = [[types.InlineKeyboardButton(text="Написать продовцу", url=f'https://t.me/{chickens[i][2]}')]]
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
                await message.answer(f'Название: {chickens[i][0]}\n'
                                     f'Адрес: {chickens[i][1]}\n'
                                     f'Тел.: +{chickens[i][2]}', reply_markup=keyboard)
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
                find_flag = 1
        if find_flag == 0:
            await message.answer('Не могу найти данную позицию.')
            await message.answer(f'Попробуйте ввести другое название или выберите другой пункт меню, '
                                 f'для этого введите /menu.')
            users[str(message.from_user.id)][0] = 'chickens'
    elif users[str(message.from_user.id)][0] == 'contacts':
        f = 0
        find_flag = 0
        for i in range(len(contacts)):
            if contacts[i][0].lower().find(message.text.lower()) != -1:
                if f == 0:
                    await message.answer('Найдены следующие варианты:')
                    f = 1
                await message.answer(f'{contacts[i][0]}  {contacts[i][1]}')
                find_flag = 1
        if find_flag == 0:
            await message.answer('Не могу найти сотрудника.')
            await message.answer(f'Попробуйте ввести другое название или выберите другой пункт меню, '
                                 f'для этого введите /menu.')
            users[str(message.from_user.id)][0] = 'contacts'
    else:
        await message.answer(f'Простите, я вас не понимаю\nЧтобы вызвать окно помощи, напишите /help')
        users[str(message.from_user.id)][0] = 'other'
    users[str(message.from_user.id)][1] = time.time()

async def main():
    bot = Bot(token='XXX')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
