import re
from typing import Any
import cv2
import configparser
import logging

from dispatcher import bot, dp
from keyboards import share_keyboard, choose_language, add_comp, no_photo, Continue
from states import UserStates

from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, CallbackQuery, Message, InputMediaAnimation, InputFile, InputMediaVideo
from aiogram.dispatcher.filters.state import State

from datetime import datetime
from pyzbar.pyzbar import decode

from db import Database
from repository import User, Ticket, Atm
from lang import get_language
from categories import cart, cashout, exchange


# database
config_file = 'config.ini'
db = Database(config_file)
ticket = Ticket(db)
user = User(db)
atm = Atm(db)

# config.ini
config = configparser.ConfigParser()
config.read(config_file)

GROUP_ID = config.get('bot', 'group_id')
TOKEN = config.get('bot', 'token')

# Configure logging
logging.basicConfig(level=logging.INFO)

# # # # # # # # # # # # # # # # # #
# helper methods
# # # # # # # # # # # # # # # # # #

async def handle_category_callback(call_data: str, state: FSMContext, category: int):
    if category == 1:
        if call_data == "enter":
            await UserStates.Q9.set()
        elif call_data == "no_photo":
            await UserStates.Q4.set()
    elif category == 2:
        if call_data == "enter":
            await UserStates.Q10.set()
        elif call_data == "no_photo":
            await UserStates.Q8.set()
    elif category == 3:
        if call_data == "enter":
            await UserStates.Q12.set()
        elif call_data == "no_photo":
            await UserStates.Q13.set()

# # # # # # # # # # # # # # # # # #
# Registration and Auth
# # # # # # # # # # # # # # # # # #

@dp.message_handler(commands="start", state='*')
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    chat_id = message.chat.id
    print(user_id)

    if user.admin_exists(user_id):
        await bot.send_message(chat_id=chat_id, text="🇷🇺Сюда вам будут приходить жалобы и предложения по вашему региону \n🇺🇿Bu erda sizning mintaqangiz bo'yicha shikoyatlar va takliflar keladi")
    elif not user.exists(user_id):
        print('not')
        await UserStates.NotExist.set()
        await bot.send_message(chat_id=chat_id, text="🇷🇺Выберите язык \n🇺🇿Tilni tanlang", reply_markup=choose_language())
    else:
        print('yes')
        await UserStates.Exist.set()
        await state.update_data(user_id=user_id)
        await bot.send_message(chat_id=message.chat.id, text="🇷🇺Выберите язык \n🇺🇿Tilni tanlang", reply_markup=choose_language())

@dp.callback_query_handler( text= ["Ru","Uz"] ,state=[UserStates.Exist, UserStates.NotExist])
async def select_lang(call: CallbackQuery, state: FSMContext):
    m = await state.get_state()

    await call.answer('Done')
    language = get_language(call.data)

    if language is not None:

        await state.update_data(language=language)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language['7'])

        if m == 'UserStates:Exist':
            msg = await bot.send_message(chat_id=call.message.chat.id, text=language['2'], reply_markup=add_comp(language['5'], language['11'], language['14']))
            await state.update_data(button=msg.message_id)
        elif m == 'UserStates:NotExist':
            msg = await bot.send_message(chat_id=call.message.chat.id, text=language['1'], reply_markup=share_keyboard())
            await state.update_data(lang_msg_id=msg.message_id)

@dp.message_handler(content_types=ContentType.CONTACT, state='*')
async def get_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    name = message.from_user.full_name
    user_id = message.from_user.id

    await state.update_data(user_id=user_id)
    user.add(name, phone, user_id)

    print('yey')

    temp_data = await state.get_data()
    message_id = temp_data.get('lang_msg_id')

    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    await bot.delete_message(chat_id=user_id, message_id=message_id)

    language = temp_data.get('language')

    msg = await bot.send_message(chat_id=message.chat.id, text=language['2'], reply_markup=add_comp(language['5'], language['11'], language['14']))
    await state.update_data(button=msg.message_id)


# # # # # # # # # # # # # # # # # #
# ?
# # # # # # # # # # # # # # # # # #

@dp.callback_query_handler(text=["add", "cashout", "card"], state='*')
async def choose_device(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    if call.data == "add":
        await state.update_data(category=1)
    elif call.data == "cashout":
        await state.update_data(category=3)
    elif call.data == "card":
        await state.update_data(category=2)

    temp_data = await state.get_data()
    language = temp_data.get('language')

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    file2 = open('instruction.MP4', 'rb')

    msg = await bot.send_animation( chat_id=call.message.chat.id, animation= file2, caption=language['8'], reply_markup=no_photo(language['9'], language['12']))

    await state.update_data(no_photo_button_message_id=msg.message_id)
    await UserStates.Q6.set()

@dp.callback_query_handler(text=["enter", "noPhoto"], state='*')
async def device_processing(call: CallbackQuery, state: FSMContext):
    

    temp_data = await state.get_data()
    language = temp_data.get('language')
    category = temp_data.get('category')
    print('noph')
    if call.data == "enter":
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id, text=language['13'])
        await UserStates.Q9.set()
    elif call.data == "noPhoto":
        print('nophoto')
        await state.update_data(exist_photo=0)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id, text=language['3'])
        await UserStates.Q4.set()

    # handle_category_callback(call.data, state, category)

@dp.callback_query_handler(text='cont', state='*')
async def device_processing(call: CallbackQuery, state: FSMContext):
    temp_data = await state.get_data()
    language = temp_data.get('language')

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = language['6'] )

    msg = await bot.send_message(chat_id=call.message.chat.id, text=language['2'], reply_markup=add_comp(language['5'], language['11'], language['14']))
    await state.update_data(button=msg.message_id)

@dp.message_handler(state=UserStates.Q9)
async def enter(message: Message, state: FSMContext):
    temp_data = await state.get_data()
    language = temp_data.get('language')
    serial_number = message.text

    region = atm.read(str(serial_number))
    print(region) 

    if len(region) != 0:
        await state.update_data(exist_photo=1)
        await state.update_data(serial_num=serial_number)
        await bot.send_message(chat_id=message.chat.id, text=language['3'])
        await UserStates.Q4.set()
    else:
        msg = await bot.send_message(chat_id=message.chat.id, text=language['15'], reply_markup=no_photo(language['9'], language['12']))
        await state.update_data(no_photo_button_message_id=msg.message_id)
        await UserStates.Q6.set()

@dp.message_handler(content_types=ContentType.PHOTO, state=UserStates.Q6)
async def get_photo(message: Message, state: FSMContext):
    await message.photo[-1].download('qrcode.jpg')

    imgQRcode = cv2.imread('qrcode.jpg')
    barcodes = decode(imgQRcode)

    temp_data = await state.get_data()
    language = temp_data.get('language')
    message_id = temp_data.get('no_photo_button_message_id')
    category = temp_data.get('category')

    if barcodes:
        serial_num = barcodes[0].data.decode('utf-8')[42:]

        await state.update_data(exist_photo=1, serial_num=serial_num)
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id)
        await bot.send_message(chat_id=message.chat.id, text=language['3'])
        await UserStates.Q4.set()
        # handle_category_callback('enter', state, category)
    else:
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id)

        msg = await bot.send_message(chat_id=message.chat.id, text=language['10'], reply_markup=no_photo(language['9'], language['12']))
        await state.update_data(no_photo_button_message_id=msg.message_id)
        await UserStates.Q6.set()


@dp.message_handler(state=UserStates.Q4)
async def complaint(message: Message, state: FSMContext):
    temp_data = await state.get_data()
    language = temp_data.get('language')
    exist_photo = temp_data.get('exist_photo')
    serial_num = temp_data.get('serial_num')

    uinfo = user.info(message.chat.id)
    uinfoCut = uinfo[0]
    com = message.text.replace("'", "''")

    current_hour = datetime.now().hour
    current_day = datetime.now().weekday()

    if current_hour < 9 or current_hour >= 18 or current_day > 5:
        await bot.send_message(message.chat.id, language['6'], reply_markup=Continue(language['16']))
    else:
        await bot.send_message(message.chat.id, language['4'], reply_markup=Continue(language['16']))

    cats = []
    categories = [cart, cashout, exchange]

    for category in categories:
        result = re.findall('|'.join(category), com)
        if len(result) != 0:
            cats.append(category[0])

    user_id = message.from_user.id

    if exist_photo == 0:
        await bot.send_message(chat_id=GROUP_ID, text='<b>' + str(uinfoCut[0]) + '</b> (' + uinfoCut[1] + ')' + '\n' + message.text)
    else:
        atm_data = atm.read(str(serial_num))
        print(atm_data)
        region = atm_data[0]
        TerminalID = atm_data[0]
        Location = atm_data[0]

        print(GROUP_ID)
        

        await bot.send_message(chat_id=GROUP_ID, text='<b>' + str(uinfoCut[0]) + '</b> (' + uinfoCut[1] + ')' + '\n' + '<b>' + 'Region: ' + str(region[1]) + '\n' + 'Terminal ID: ' + str(TerminalID[2]) + '\n' + 'Location: ' + str(Location[5]) + '</b>' + '\n' + message.text)
        print(str(region[1]))
        chat_id = user.admin_by_state(str(region[1]))
        chat_idCut = chat_id[0]
        print(chat_idCut)
        for i in chat_idCut:
            print(i)
            await bot.send_message(chat_id=str(i), text='<b>' + str(uinfoCut[0]) + '</b> (' + uinfoCut[1] + ')' + '\n' + '<b>' + 'Region: ' + str(region[1]) + '\n' + 'Terminal ID: ' + str(TerminalID[2]) + '\n' + 'Location: ' + str(Location[5]) + '</b>' + '\n' + message.text)

    if len(cats) == 0:
        cats.append('other')

    tempCategoria = await state.get_data('category')
    categoria = tempCategoria['category']
    print(categoria)

    if categoria == 1:
        ticket.add_status(user_id, com, 'Другое', '-' if exist_photo == 0 else serial_num)
    elif categoria == 2:
        ticket.add_status(user_id, com, 'Банкомат захватил карту', '-' if exist_photo == 0 else serial_num)
    elif categoria == 3: 
        ticket.add_status(user_id, com, 'Проблемы с выдачей наличных', '-' if exist_photo == 0 else serial_num)
# END

@dp.message_handler(content_types=ContentType.ANY, state='*')
async def chat_free(message: Message):
    if message.chat.id != GROUP_ID:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
