###############################################################################
from random import randint

import logging
from aiogram import Bot, Dispatcher
from aiogram import types
from categories import cart, cashout, exchange
import re

from datetime import datetime
import pytz

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram.types import ContentType, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton


import cv2
import numpy as np
from pyzbar.pyzbar import decode
# from PIL import Image

GROUP_ID = -1001905509764
# Configure logging
logging.basicConfig(level=logging.INFO)


# init
bot = Bot(token='6256030003:AAHt1Ui_MZFEkz7wngxLabxoeihRx4Fn-lg', parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

################################################################################

################################################################################

import sqlite3
import mysql.connector as mariadb
from mysql.connector import Error

try:
    con = mariadb.connect(user= 'test', password = '@bvMT2j0Q05q', host = '68.183.75.13', port = '3306', db = 'SupportBot')
except Error as e:
    print(f"Error connecting to MySQL database: {e}")


try:
    cur = con.cursor()
except mariadb.Error as e:
    if isinstance(e, mariadb.errors.InterfaceError) and "Connection reset by peer" in str(e):
        print("Connection reset by peer. Reconnecting...")
        try:
            con = mariadb.connect(user= 'test', password = '@bvMT2j0Q05q', host = '68.183.75.13', port = '3306', db = 'SupportBot')
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
    else:
        print(f"Error executing query: {e}")
                

def user_info(user_id):
    q = "SELECT * FROM user WHERE Id = '%s'" % (str(user_id),)
    result = cur.execute(q)
    result = cur.fetchone()

    return result

def user_exists(user_id):
    q = "SELECT Id FROM user WHERE Id = '%s'" % (str(user_id),)
    print(q)
    result = cur.execute(q)
    result = cur.fetchall()
    print(result)

    return bool(len(result))

def admin_exists(user_id):
    q = "SELECT admin FROM admins WHERE admin = '%s'" % (str(user_id),)
    print(q)
    result = cur.execute(q)
    result = cur.fetchall()
    print(result)

    return bool(len(result))

def add_user(name, num, user_id):

    cur.execute("INSERT INTO user (Name, Phone, Id) VALUES ('%s', '%s', '%d')" % (name, num, user_id) )
    
    con.commit()

def num_exists(num):
    result = cur.execute("SELECT `num` FROM `ticket` WHERE `num` = ?", (str(num),))

    return bool(len(result.fetchall()))    

def add_status(user_id, com, cats, serialNum):

    sql = "INSERT INTO ticket (userid, message, category, serial) VALUES ('%d', '%s', '%s', '%s')"
    data = (user_id, com, cats, serialNum)

    cur.execute(sql % data)
    # cur.execute("INSERT INTO ticket (userid, message) VALUES ('%d', '%s')" % (user_id, com) )
    
    con.commit()


def change_status( num, status ):

    cur.execute("UPDATE ticket SET status = ? WHERE num = ?" % (status), (num))

    con.commit()

# def findTickets( user_id ):

#     cur.execute("SELECT `num` FROM `ticket` WHERE `userid` = ?", (str(user_id),))
#     cur.fetchall()

################################################################################

################################################################################

from aiogram.dispatcher.filters.state import StatesGroup, State

class userStates(StatesGroup):
    
    Registration = State() 
    Complaint = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()
    Q6 = State()
    Q7 = State()
    Q8 = State()
    Q9 = State()
    Q10 = State()
    Q11 = State()
    Q12 = State()
    Q13 = State()
    exist = State()
    notExist = State()

################################################################################

################################################################################

from aiogram.dispatcher import FSMContext
from aiogram import types
from dict import ruDictionary, uzDictionary

share_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
share_button = types.KeyboardButton(text="📱 Отправить", request_contact=True)
share_keyboard.add(share_button)

def chooseLanguage():
 
    buttons = [
        types.InlineKeyboardButton(text="Ru", callback_data="Ru"),
        types.InlineKeyboardButton(text="Uz", callback_data="Uz"),
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

    #ПРИ НАЖАТИИ КНОПКИ СТАРТ ИДЕТ ВЫБОР ЯЗЫКА И В ПОСЛЕДУЮЩЕМ ВСЕ ТЕКСТЫ БУДУТ ВЫВОДИТЬСЯ ИЗ ОПРНДНЛНННОГО СЛОВАРЯ КОТОРЫЙ ВЫБРАЛ ПОЛЬЗОВАТЕЛЬ
    #В СЛУЧАЕ ЕСЛИ БОТ БЫЛ ПЕРЕЗАПУЩЕН И ПОЛЬЗОВАТЕЛЬ НЕ НАЖАЛ КНОПКУ СТАРТ И НЕ ВЫБРАЛ ЯЗЫК ЗАНОВО ВЫХОДИТ ОШИБКА, БОТ НЕ ПОНИМАЕТ НА КАКОМ ЯЗЫКЕ ВЫДАВАТЬ ТЕКСТ
    #МОЖНО РЕШИТЬ СОХРАНЯЯ ЯЗЫК ПОЛЬЗОВАТЕЛЯ В БД

@dp.message_handler(commands = "start", state= '*' )
async def start(message: types.Message, state: FSMContext):
    userid = message.from_user.id
    # await bot.delete_message(chat_id=userid, message_id=message.message_id)

    if(admin_exists(message.from_user.id)):
        await bot.send_message( chat_id = message.chat.id, text = "🇷🇺Сюда вам будут приходить жалобы и предложения по вашему региону \n🇺🇿Bu erda sizning mintaqangiz bo'yicha shikoyatlar va takliflar keladi" )


    elif(not user_exists(message.from_user.id)):

        forId1 = await bot.send_message( chat_id = message.chat.id, text ="🇷🇺Выберите язык \n🇺🇿Tilni tanlang", reply_markup=chooseLanguage())
        id1 = forId1.message_id
        print('22222222222222222222222222222222222222')
        await userStates.notExist.set()
        @dp.callback_query_handler(text = "Ru", state=userStates.notExist)
        async def message_handler(call: types.CallbackQuery, state: FSMContext):
            await call.answer('Done')
            language = ruDictionary
            await state.update_data(language=language)
            
            await bot.edit_message_text( chat_id = call.message.chat.id, message_id= call.message.message_id, text= language['7'] )

            m = await bot.send_message( chat_id = call.message.chat.id, text =language['1'], reply_markup=share_keyboard)
            id = m.message_id
            await state.update_data(Id1=id)

        @dp.callback_query_handler(text = "Uz", state= userStates.notExist)
        async def message_handler(call: types.CallbackQuery, state: FSMContext):
            await call.answer('Done')
            language = uzDictionary
            await state.update_data(language=language)

            await bot.edit_message_text( chat_id = call.message.chat.id, message_id= call.message.message_id, text= language['7'] )

            m = await bot.send_message( chat_id = call.message.chat.id, text = language['1'], reply_markup=share_keyboard)
            id = m.message_id
            await state.update_data(Id1=id)

    else:
        await state.update_data(userId=userid)
        print('11111111111111111111111111111111111111111111111111111111111111111111111111111')
        await userStates.exist.set()
        forId1 = await bot.send_message( chat_id = message.chat.id, text = "🇷🇺Выберите язык \n🇺🇿Tilni tanlang", reply_markup=chooseLanguage())
        id1 = forId1.message_id

        @dp.callback_query_handler(text = "Ru", state= userStates.exist)
        async def message_handler(call: types.CallbackQuery, state: FSMContext):
            await call.answer('Done')

            language = ruDictionary
            await state.update_data(language=language)
            
            await bot.edit_message_text( chat_id = call.message.chat.id, message_id= call.message.message_id, text= language['7'] )

            m = await bot.send_message( chat_id = call.message.chat.id, text = language['2'], reply_markup=addComp(language['5'], language['11'], language['14']))
            id = m.message_id
            await state.update_data(button=id)
            await userStates.Q3.set()

        @dp.callback_query_handler(text = "Uz", state= userStates.exist)
        async def message_handler(call: types.CallbackQuery, state: FSMContext):
            await call.answer('Done')
            language = uzDictionary
            await state.update_data(language=language)

            await bot.edit_message_text( chat_id = call.message.chat.id, message_id= call.message.message_id, text= language['7'] )

            m = await bot.send_message( chat_id = call.message.chat.id, text = language['2'], reply_markup=addComp(language['5'], language['11'], language['14']))
            id = m.message_id
            await state.update_data(button=id)
            await userStates.Q3.set()
       



@dp.message_handler(content_types=types.ContentType.CONTACT, state='*')
async def get_contact(message: types.Message, state: FSMContext):

    phone = message.contact.phone_number
    name = message.from_user.full_name
    userid = message.from_user.id

    await state.update_data(userId=userid)

    add_user(name, phone, userid)

    temp = await state.get_data('Id1')
    messageId = temp['Id1']

    await bot.delete_message(chat_id=userid, message_id=message.message_id)
    await bot.delete_message(chat_id=userid, message_id=messageId)

    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']

    m = await bot.send_message( chat_id = message.chat.id, text = language['2'], reply_markup=addComp(language['5'], language['11'], language['14']))

    id = m.message_id
    await state.update_data(button=id)

    await userStates.Q3.set()

################################################################################

################################################################################

    #КОЛБЭКИ ADD, CASHOUT И CARD ОТЛИЧАЮТСЯ ТОЛЬКО ВЫБОРОМ КАТЕГОРИИ ПОЛЬЗОВАТЕЛЕМ, НО ФУНКЦИОНАЛ ПОЛНОСТЬЮ ИДЕНТИЧЕН
    #МОЖНО НЕ ПРОПИСЫВАТЬ ФУНКЦИОНАЛ В КАЖДОМ КОЛБЭКЕ, А ВЫВЕСТИ ОТДЕЛЬНО
    #КОД ЗАХЛАМЛЯЕТСЯ

@dp.callback_query_handler(text = "add", state='*')
async def message_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await state.update_data(categoria=1)
    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
   
    m = await bot.send_message( chat_id = call.message.chat.id, text = language['8'], reply_markup=noPhoto(language['9'], language['12']))
    noPhotoButton = m.message_id
    await state.update_data(photoButton=noPhotoButton)
    await userStates.Q6.set()

    @dp.callback_query_handler(text = "enter", state='*')
    async def message_handler(call: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        # await bot.send_photo(chat_id=call.message.chat.id, photo=open('instruction.jpg', 'rb'))   
        await bot.send_message( chat_id = call.message.chat.id, text = language['13'])  
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await userStates.Q9.set()
        if categoria == 2:
            await userStates.Q10.set()
        if categoria == 3:
            await userStates.Q12.set()

    #КАК РАЗ ИЗ-ЗА ТОГО ЧТО У ТРЕХ ОСНОВНЫХ КОЛБЭКОВ МИНИМАЛЬНО РАЗЛИЧАЮЩИЙСЯ ФУНКЦИОНАЛ ПРИШЛОСЬ ДОБАВИТЬ КУЧУ РАЗНЫХ СОСТОЯНИХ
    #ЧТОБЫ БОТ ОРИЕНИРОВАЛСЯ В НИХ
    #КОЛБЭКИ ВНУТРИ КОЛБЭКОВ ТАКЖЕ ЯВЛЯЮТСЯ ПРОБЛЕМОЙ

    @dp.callback_query_handler(text = "noPhoto", state='*')
    async def message_handler(call: types.CallbackQuery, state: FSMContext):
        await state.update_data(existPhoto=0)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language['3'])
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await userStates.Q4.set()
        if categoria == 2:
            await userStates.Q8.set()
        if categoria == 3:
            await userStates.Q13.set()        

@dp.message_handler(state=userStates.Q9)
async def enter(message: types.Message, state: FSMContext):
    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']
    s = message.text

    q = "SELECT State FROM atm WHERE UniqueID = '%s'" % (str(s),)
    region = cur.execute(q)
    region = cur.fetchall()

    if len(region) != 0:
        await state.update_data(existPhoto=1)
        await state.update_data(serialNum=s)
        await bot.send_message( chat_id = message.chat.id, text = language['3'])
        await userStates.Q4.set()
    else:
        m = await bot.send_message( chat_id= message.chat.id, text= language['15'], reply_markup= noPhoto(language['9'], language['12']) )        
        noPhotoButton = m.message_id
        await state.update_data(photoButton=noPhotoButton)
        await userStates.Q6.set()

    #ФОТО QR КОДА ОТПРАВЛЯЕМОЕ ПОЛЬЗОВАТЕЛЕМ СОХРАНЯЕТСЯ В ТОЙ ЖЕ ПАПКЕ ПОД ТЕМ ЖЕ НАЗВАНИЕМ
    #СУЩЕСТВУЕТ ВОЗМОЖНОСТЬ ВОЗНИКНОВЕНИЯ ОШИБКИ ЕСЛИ ДВА ПОЛЬЗОВАТЕЛЯ ОТПРАВЛЯЮТ ФОТОГРАФИИ ОДНОВРЕМЕННО (ХОТЯ Я ПРОВЕРЯЛ, ОШИБОК НЕ ВОЗНИКАЛО)
    #ПРЕДПОЛАГАЕМОЕ РЕШЕНИЕ: СОХРАНЯТЬ ФОТО С НАЗВАНИЕМ В ВИДЕ USERID ПОЛЬЗОВАТЕЛЯ ОТПРАВИВШЕГО ЕГО. ТОГДА ВНУТРИ ЛОГИКИ БОТА НЕ БУДЕТ ВОЗНИКАТЬ ПУТАНИЦЫ

@dp.message_handler(content_types=types.ContentType.PHOTO, state=userStates.Q6)
async def get_photo(message: types.Message, state: FSMContext):    

    await message.photo[-1].download('qrcode.jpg')

    
    # result = decode(Image.open('qrcode.png'))
    # print(result)
    imgQRcode = cv2.imread('qrcode.jpg')
    code = decode(imgQRcode)
    print(code)
    print(len(code))

    for barcode in decode(imgQRcode):
        data = barcode.data.decode('utf-8')
        print(data)



    if len(code) != 0:
        size = 42
        c = data[size]
        s = c
        
        while size != len(data)-1:
            size = size + 1
            c = data[size]
            s = s + c
            

        await state.update_data(existPhoto=1)
        await state.update_data(serialNum=s)
        tempForLanguage = await state.get_data('language')
        language = tempForLanguage['language']

        temp = await state.get_data('photoButton')
        messegeId = temp['photoButton']

        await bot.edit_message_text(chat_id=message.chat.id, message_id=messegeId, text=language['8'])
        
        await bot.send_message( chat_id = message.chat.id, text = language['3'])
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await userStates.Q4.set()
        if categoria == 2:
            await userStates.Q8.set()
        if categoria == 3:
            await userStates.Q13.set()

    else:

        tempForLanguage = await state.get_data('language')
        language = tempForLanguage['language']

        temp = await state.get_data('photoButton')
        messegeId = temp['photoButton']

        await bot.edit_message_text(chat_id=message.chat.id, message_id=messegeId, text=language['8'])

        m = await bot.send_message( chat_id = message.chat.id, text = language['10'], reply_markup=noPhoto(language['9'], language['12']))
        noPhotoButton = m.message_id
        await state.update_data(photoButton=noPhotoButton)
        await userStates.Q6.set()

        @dp.callback_query_handler(text = "enter", state='*')
        async def message_handler(call: types.CallbackQuery, state: FSMContext):
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            # await bot.send_photo(chat_id=call.message.chat.id, photo=open('instruction.jpg', 'rb'))   
            await bot.send_message( chat_id = call.message.chat.id, text = language['13'])  
            tempCategoria = await state.get_data('categoria')
            categoria = tempCategoria['categoria']
            if categoria == 1:
                await userStates.Q9.set()
            if categoria == 2:
                await userStates.Q10.set()
            if categoria == 3:
                await userStates.Q12.set()

        @dp.callback_query_handler(text = "noPhoto", state='*')
        async def message_handler(call: types.CallbackQuery, state: FSMContext):
            await state.update_data(existPhoto=0)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language['3'])
            tempCategoria = await state.get_data('categoria')
            categoria = tempCategoria['categoria']
            if categoria == 1:
                await userStates.Q4.set()
            if categoria == 2:
                await userStates.Q8.set()
            if categoria == 3:
                await userStates.Q13.set()


@dp.message_handler(state=userStates.Q4)
async def Complaint(message: types.Message, state: FSMContext):
    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']

    uinfo = user_info(message.chat.id)
 
    
    com1 = message.text

    com = com1.replace("'", "''")

    # В УЗБЕКСКОМ ЯЗЫКЕ МОГУТ ВСТРЕЧАТЬСЯ СИМВОЛЫ ' Я ПРЕДУСМОТРЕЛ ЧТОБЫ ОНИ СОХРАНЯЛИСЬ В БАЗУ И ЛОГИКА НЕ ЛОМАЛАСЬ
    # НО  НЕ ПРЕДУСМОТРЕЛ "

    currentHour = datetime.now().hour

    currentDay = datetime.now().weekday()

    tempExistPhoto = await state.get_data('existPhoto')
    existPhoto = tempExistPhoto['existPhoto']

    if currentHour < 9 or currentHour >= 18 or currentDay > 5:
        await bot.send_message(message.chat.id, language['6'], reply_markup=addComp(language['5'], language['11'], language['14']))
    else:
        await bot.send_message(message.chat.id, language['4'], reply_markup=addComp(language['5'], language['11'], language['14']))

    for x in cart:
        result1 = re.findall(x, com)

    for x in cashout:
        result2 = re.findall(x, com)

    for x in exchange:
        result3 = re.findall(x, com)

    cats = []
    if len(result1)!=0:
        cats.append('cart')
    if len(result2)!=0:
        cats.append('cashout')
    if len(result3)!=0:
        cats.append('exchange')

    userid = message.from_user.id

    if existPhoto == 0:

        await bot.send_message(chat_id='-1001905509764', text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + message.text)

        if len(cats)==1:
            add_status(userid, com, cats[0], '-')

        if len(cats)==2:
            tempStr = cats[0]+','+cats[1]
            add_status(userid, com, tempStr, '-')

        if len(cats)==3:
            tempStr = cats[0]+','+cats[1]+','+cats[2]
            add_status(userid, com, tempStr, '-')

        if len(cats)==0:
            add_status(userid, com, 'other', '-')
    
    if existPhoto == 1:
        tempSerialNum = await state.get_data('serialNum')
        serialNum = tempSerialNum['serialNum']

        print('serial num: ' + str(serialNum))

        q = "SELECT State FROM atm WHERE UniqueID = '%s'" % (str(serialNum),)
        region = cur.execute(q)
        region = cur.fetchone()

        print('region: ' + str(region))

        q = "SELECT TerminalID FROM atm WHERE UniqueID = '%s'" % (str(serialNum),)
        TerminalID = cur.execute(q)
        TerminalID = cur.fetchone()

        q = "SELECT Location FROM atm WHERE UniqueID = '%s'" % (str(serialNum),)
        Location = cur.execute(q)
        Location = cur.fetchone()

        await bot.send_message(chat_id='-1001905509764', text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + '<b>' + 'Region: ' + str(region[0]) + '\n' + 'Terminal ID: ' + str(TerminalID[0]) + '\n' + 'Location: ' + str(Location[0]) + '</b>' + '\n' + message.text)

        print('serial num: ' + str(serialNum))

        q = "SELECT State FROM atm WHERE UniqueID = '%s'" % (str(serialNum),)
        region = cur.execute(q)
        region = cur.fetchone()

        print('region: ' + str(region))

        q = "SELECT admin FROM admins WHERE State = '%s'" % (str(region[0]),)
        chatId = cur.execute(q)
        chatId = cur.fetchall()

        print('chat id: ' + str(chatId))

        for i in chatId:
            await bot.send_message(chat_id=str(i[0]), text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + '<b>' + 'Region: ' + str(region[0]) + '\n' + 'Terminal ID: ' + str(TerminalID[0]) + '\n' + 'Location: ' + str(Location[0]) + '</b>' + '\n' + message.text)


        if len(cats)==1:
            add_status(userid, com, cats[0], serialNum)

        if len(cats)==2:
            tempStr = cats[0]+','+cats[1]
            add_status(userid, com, tempStr, serialNum)

        if len(cats)==3:
            tempStr = cats[0]+','+cats[1]+','+cats[2]
            add_status(userid, com, tempStr, serialNum)

        if len(cats)==0:
            add_status(userid, com, 'other', serialNum)
    

    await userStates.Q3.set()



@dp.callback_query_handler(text = "card", state='*')
async def message_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await state.update_data(categoria=2)
    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
   
    m = await bot.send_message( chat_id = call.message.chat.id, text = language['8'], reply_markup=noPhoto(language['9'], language['12']))
    noPhotoButton = m.message_id
    await state.update_data(photoButton=noPhotoButton)
    await userStates.Q7.set()

    @dp.callback_query_handler(text = "enter", state='*')
    async def message_handler(call: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        # await bot.send_photo(chat_id=call.message.chat.id, photo=open('instruction.jpg', 'rb'))   
        await bot.send_message( chat_id = call.message.chat.id, text = language['13'])  
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await userStates.Q9.set()
        if categoria == 2:
            await userStates.Q10.set()
        if categoria == 3:
            await userStates.Q12.set()

    @dp.callback_query_handler(text = "noPhoto", state='*')
    async def message_handler(call: types.CallbackQuery, state: FSMContext):
        await state.update_data(existPhoto=0)
        print('11')
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language['3'])
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await userStates.Q4.set()
        if categoria == 2:
            await userStates.Q8.set()
        if categoria == 3:
            await userStates.Q13.set()

@dp.message_handler(state=userStates.Q10)
async def enter(message: types.Message, state: FSMContext):
    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']
    s = message.text

    q = "SELECT State FROM atm WHERE UniqueID = '%s'" % (str(s),)
    region = cur.execute(q)
    region = cur.fetchall()

    if len(region) != 0:
        await state.update_data(existPhoto=1)
        await state.update_data(serialNum=s)
        await bot.send_message( chat_id = message.chat.id, text = language['3'])
        await userStates.Q8.set()
    else:
        m = await bot.send_message( chat_id= message.chat.id, text= language['15'], reply_markup= noPhoto(language['9'], language['12']) )        
        noPhotoButton = m.message_id
        await state.update_data(photoButton=noPhotoButton)
        await userStates.Q7.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=userStates.Q7)
async def get_photo(message: types.Message, state: FSMContext):    

    await message.photo[-1].download('qrcode.jpg')

    
    # result = decode(Image.open('qrcode.png'))
    # print(result)
    imgQRcode = cv2.imread('qrcode.jpg')
    code = decode(imgQRcode)
    print(code)
    print(len(code))

    for barcode in decode(imgQRcode):
        data = barcode.data.decode('utf-8')
        print(data)



    if len(code) != 0:
        size = 42
        c = data[size]
        s = c
        
        while size != len(data)-1:
            size = size + 1
            c = data[size]
            s = s + c

        await state.update_data(existPhoto=1)
        await state.update_data(serialNum=s)
        tempForLanguage = await state.get_data('language')
        language = tempForLanguage['language']

        temp = await state.get_data('photoButton')
        messegeId = temp['photoButton']

        await bot.edit_message_text(chat_id=message.chat.id, message_id=messegeId, text=language['8'])
        
        await bot.send_message( chat_id = message.chat.id, text = language['3'])
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await userStates.Q4.set()
        if categoria == 2:
            await userStates.Q8.set()
        if categoria == 3:
            await userStates.Q13.set()

    else:

        tempForLanguage = await state.get_data('language')
        language = tempForLanguage['language']

        temp = await state.get_data('photoButton')
        messegeId = temp['photoButton']

        await bot.edit_message_text(chat_id=message.chat.id, message_id=messegeId, text=language['8'])

        m = await bot.send_message( chat_id = message.chat.id, text = language['10'], reply_markup=noPhoto(language['9'], language['12']))
        noPhotoButton = m.message_id
        await state.update_data(photoButton=noPhotoButton)
        await userStates.Q6.set()

        @dp.callback_query_handler(text = "enter", state='*')
        async def message_handler(call: types.CallbackQuery, state: FSMContext):
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            # await bot.send_photo(chat_id=call.message.chat.id, photo=open('instruction.jpg', 'rb'))   
            await bot.send_message( chat_id = call.message.chat.id, text = language['13'])  
            tempCategoria = await state.get_data('categoria')
            categoria = tempCategoria['categoria']
            if categoria == 1:
                await userStates.Q9.set()
            if categoria == 2:
                await userStates.Q10.set()
            if categoria == 3:
                await userStates.Q12.set()

        @dp.callback_query_handler(text = "noPhoto", state='*')
        async def message_handler(call: types.CallbackQuery, state: FSMContext):
            await state.update_data(existPhoto=0)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language['3'])
            tempCategoria = await state.get_data('categoria')
            categoria = tempCategoria['categoria']
            if categoria == 1:
                await userStates.Q4.set()
            if categoria == 2:
                await userStates.Q8.set()
            if categoria == 3:
                await userStates.Q13.set()

@dp.message_handler(state=userStates.Q8)
async def Complaint(message: types.Message, state: FSMContext):
    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']
    print('12')
    uinfo = user_info(message.chat.id)

    com1 = message.text

    com = com1.replace("'", "''")

    currentHour = datetime.now().hour

    currentDay = datetime.now().weekday()

    tempExistPhoto = await state.get_data('existPhoto')
    existPhoto = tempExistPhoto['existPhoto']

    if currentHour < 9 or currentHour >= 18 or currentDay > 5:
        await bot.send_message(message.chat.id, language['6'], reply_markup=addComp(language['5'], language['11'], language['14']))
    else:
        await bot.send_message(message.chat.id, language['4'], reply_markup=addComp(language['5'], language['11'], language['14']))

    userid = message.from_user.id

    if existPhoto == 0:

        await bot.send_message(chat_id='-1001905509764', text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + message.text)
        add_status(userid, com, "card", '-')

    
    if existPhoto == 1:

        tempSerialNum = await state.get_data('serialNum')
        serialNum = tempSerialNum['serialNum']

        q = "SELECT State FROM atm WHERE UniqueID = '%s'" % (str(serialNum),)
        region = cur.execute(q)
        region = cur.fetchone()

        print('region: ' + str(region))

        q = "SELECT TerminalID FROM atm WHERE UniqueID = '%s'" % (str(serialNum),)
        TerminalID = cur.execute(q)
        TerminalID = cur.fetchone()

        q = "SELECT Location FROM atm WHERE UniqueID = '%s'" % (str(serialNum),)
        Location = cur.execute(q)
        Location = cur.fetchone()

        await bot.send_message(chat_id='-1001905509764', text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + '<b>' + 'Region: ' + str(region[0]) + '\n' + 'Terminal ID: ' + str(TerminalID[0]) + '\n' + 'Location: ' + str(Location[0]) + '</b>' + '\n' + message.text)

        print('serial num: ' + str(serialNum))

        q = "SELECT State FROM atm WHERE UniqueID = '%s'" % (str(serialNum),)
        region = cur.execute(q)
        region = cur.fetchone()

        print('region: ' + str(region))

        q = "SELECT admin FROM admins WHERE State = '%s'" % (str(region[0]),)
        chatId = cur.execute(q)
        chatId = cur.fetchall()

        print('chat id: ' + str(chatId))

        for i in chatId:
            await bot.send_message(chat_id=str(i[0]), text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + '<b>' + 'Region: ' + str(region[0]) + '\n' + 'Terminal ID: ' + str(TerminalID[0]) + '\n' + 'Location: ' + str(Location[0]) + '</b>' + '\n' + message.text)


        tempSerialNum = await state.get_data('serialNum')
        serialNum = tempSerialNum['serialNum']
        add_status(userid, com, "card", serialNum)

    

    await userStates.Q3.set()

@dp.callback_query_handler(text = "cashout", state='*')
async def message_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer('Done')

    await state.update_data(categoria=3)

    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
   
    m = await bot.send_message( chat_id = call.message.chat.id, text = language['8'], reply_markup=noPhoto(language['9'], language['12']))
    noPhotoButton = m.message_id
    await state.update_data(photoButton=noPhotoButton)
    await userStates.Q11.set()

    @dp.callback_query_handler(text = "enter", state='*')
    async def message_handler(call: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        # await bot.send_photo(chat_id=call.message.chat.id, photo=open('instruction.jpg', 'rb'))   
        await bot.send_message( chat_id = call.message.chat.id, text = language['13'])  
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await userStates.Q9.set()
        if categoria == 2:
            await userStates.Q10.set()
        if categoria == 3:
            await userStates.Q12.set()

    @dp.callback_query_handler(text = "noPhoto", state='*')
    async def message_handler(call: types.CallbackQuery, state: FSMContext):
        await state.update_data(existPhoto=0)
        print('1111')
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language['3'])
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await userStates.Q4.set()
        if categoria == 2:
            await userStates.Q8.set()
        if categoria == 3:
            await userStates.Q13.set()

@dp.message_handler(state=userStates.Q12)
async def enter(message: types.Message, state: FSMContext):
    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']
    s = message.text

    q = "SELECT State FROM atm WHERE UniqueID = '%s'" % (str(s),)
    region = cur.execute(q)
    region = cur.fetchall()

    if len(region) != 0:
        await state.update_data(existPhoto=1)
        await state.update_data(serialNum=s)
        await bot.send_message( chat_id = message.chat.id, text = language['3'])
        await userStates.Q13.set()
    else:
        m = await bot.send_message( chat_id= message.chat.id, text= language['15'], reply_markup= noPhoto(language['9'], language['12']) )        
        noPhotoButton = m.message_id
        await state.update_data(photoButton=noPhotoButton)
        await userStates.Q11.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=userStates.Q11)
async def get_photo(message: types.Message, state: FSMContext):    

    await message.photo[-1].download('qrcode.jpg')

    
    # result = decode(Image.open('qrcode.png'))
    # print(result)
    imgQRcode = cv2.imread('qrcode.jpg')
    code = decode(imgQRcode)
    print(code)
    print(len(code))

    for barcode in decode(imgQRcode):
        data = barcode.data.decode('utf-8')
        print(data)



    if len(code) != 0:
        size = 42
        c = data[size]
        s = c
        
        while size != len(data)-1:
            size = size + 1
            c = data[size]
            s = s + c

        await state.update_data(existPhoto=1)
        await state.update_data(serialNum=s)
        tempForLanguage = await state.get_data('language')
        language = tempForLanguage['language']

        temp = await state.get_data('photoButton')
        messegeId = temp['photoButton']

        await bot.edit_message_text(chat_id=message.chat.id, message_id=messegeId, text=language['8'])
        
        await bot.send_message( chat_id = message.chat.id, text = language['3'])
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await userStates.Q4.set()
        if categoria == 2:
            await userStates.Q8.set()
        if categoria == 3:
            await userStates.Q13.set()

    else:

        tempForLanguage = await state.get_data('language')
        language = tempForLanguage['language']

        temp = await state.get_data('photoButton')
        messegeId = temp['photoButton']

        await bot.edit_message_text(chat_id=message.chat.id, message_id=messegeId, text=language['8'])

        m = await bot.send_message( chat_id = message.chat.id, text = language['10'], reply_markup=noPhoto(language['9'], language['12']))
        noPhotoButton = m.message_id
        await state.update_data(photoButton=noPhotoButton)
        await userStates.Q6.set()

        @dp.callback_query_handler(text = "enter", state='*')
        async def message_handler(call: types.CallbackQuery, state: FSMContext):
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            # await bot.send_photo(chat_id=call.message.chat.id, photo=open('instruction.jpg', 'rb'))   
            await bot.send_message( chat_id = call.message.chat.id, text = language['13'])  
            tempCategoria = await state.get_data('categoria')
            categoria = tempCategoria['categoria']
            if categoria == 1:
                await userStates.Q9.set()
            if categoria == 2:
                await userStates.Q10.set()
            if categoria == 3:
                await userStates.Q12.set()

        @dp.callback_query_handler(text = "noPhoto", state='*')
        async def message_handler(call: types.CallbackQuery, state: FSMContext):
            await state.update_data(existPhoto=0)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language['3'])
            tempCategoria = await state.get_data('categoria')
            categoria = tempCategoria['categoria']
            if categoria == 1:
                await userStates.Q4.set()
            if categoria == 2:
                await userStates.Q8.set()
            if categoria == 3:
                await userStates.Q13.set()

@dp.message_handler(state=userStates.Q13)
async def Complaint(message: types.Message, state: FSMContext):
    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']
    print('1122')
    uinfo = user_info(message.chat.id)
 
    com1 = message.text

    com = com1.replace("'", "''")

    currentHour = datetime.now().hour

    currentDay = datetime.now().weekday()

    tempExistPhoto = await state.get_data('existPhoto')
    existPhoto = tempExistPhoto['existPhoto']

    if currentHour < 9 or currentHour >= 18 or currentDay > 5:
        await bot.send_message(message.chat.id, language['6'], reply_markup=addComp(language['5'], language['11'], language['14']))
    else:
        await bot.send_message(message.chat.id, language['4'], reply_markup=addComp(language['5'], language['11'], language['14']))

    userid = message.from_user.id

    if existPhoto == 0:

        await bot.send_message(chat_id='-1001905509764', text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + message.text)
        add_status(userid, com, "cashout", '-')

    
    if existPhoto == 1:

        tempSerialNum = await state.get_data('serialNum')
        serialNum = tempSerialNum['serialNum']

        print('serial num: ' + str(serialNum))

        q = "SELECT State FROM atm WHERE UniqueID = '%s'" % (str(serialNum),)
        region = cur.execute(q)
        region = cur.fetchone()

        print('region: ' + str(region))

        q = "SELECT TerminalID FROM atm WHERE UniqueID = '%s'" % (str(serialNum),)
        TerminalID = cur.execute(q)
        TerminalID = cur.fetchone()

        q = "SELECT Location FROM atm WHERE UniqueID = '%s'" % (str(serialNum),)
        Location = cur.execute(q)
        Location = cur.fetchone()

        await bot.send_message(chat_id='-1001905509764', text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + '<b>' + 'Region: ' + str(region[0]) + '\n' + 'Terminal ID: ' + str(TerminalID[0]) + '\n' + 'Location: ' + str(Location[0]) + '</b>' + '\n' + message.text)

        print('serial num: ' + str(serialNum))

        q = "SELECT State FROM atm WHERE UniqueID = '%s'" % (str(serialNum),)
        region = cur.execute(q)
        region = cur.fetchone()

        print('region: ' + str(region))

        q = "SELECT admin FROM admins WHERE State = '%s'" % (str(region[0]),)
        chatId = cur.execute(q)
        chatId = cur.fetchall()

        print('chat id: ' + str(chatId))

        for i in chatId:
            await bot.send_message(chat_id=str(i[0]), text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + '<b>' + 'Region: ' + str(region[0]) + '\n' + 'Terminal ID: ' + str(TerminalID[0]) + '\n' + 'Location: ' + str(Location[0]) + '</b>' + '\n' + message.text)

        tempSerialNum = await state.get_data('serialNum')
        serialNum = tempSerialNum['serialNum']
        add_status(userid, com, "cashout", serialNum)

    

    await userStates.Q3.set()

     

################################################################################

################################################################################

def addComp(textForAdd, textForCard, textForCashOut):
 
    buttons = [
        types.InlineKeyboardButton(text=textForCard, callback_data="card"),
        types.InlineKeyboardButton(text=textForCashOut, callback_data="cashout"),
        types.InlineKeyboardButton(text=textForAdd, callback_data="add"),
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

def noPhoto(textForAdd, textForEnter):
 
    buttons = [
        types.InlineKeyboardButton(text=textForAdd, callback_data="noPhoto"),
        types.InlineKeyboardButton(text=textForEnter, callback_data="enter"),

    ]

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

################################################################################
@dp.message_handler(content_types=types.ContentType.ANY, state= '*' )
async def Complaint(message: types.Message):
    if message.chat.id != GROUP_ID:
        await bot.delete_message( chat_id=message.chat.id, message_id= message.message_id )
################################################################################


from aiogram import executor

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

################################################################################
