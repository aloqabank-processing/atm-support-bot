import re
import cv2
import configparser
import logging

from main import bot, dp
from keyboards import share_keyboard, choose_language, add_comp, no_photo
from states import UserStates

from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, CallbackQuery, Message

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

################################################################################

################################################################################


@dp.message_handler(commands="start", state='*')
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if user.admin_exists(user_id):
        await bot.send_message(chat_id=chat_id, text="🇷🇺Сюда вам будут приходить жалобы и предложения по вашему региону \n🇺🇿Bu erda sizning mintaqangiz bo'yicha shikoyatlar va takliflar keladi")
    elif not user.exists(user_id):
        await UserStates.NotExist.set()
        await bot.send_message(chat_id=chat_id, text="🇷🇺Выберите язык \n🇺🇿Tilni tanlang", reply_markup=choose_language())
    else:
        await UserStates.Exist.set()
        await state.update_data(userId=user_id)
        await bot.send_message(chat_id=message.chat.id, text="🇷🇺Выберите язык \n🇺🇿Tilni tanlang", reply_markup=choose_language())

@dp.callback_query_handler(state=[UserStates.Exist, UserStates.NotExist])
async def select_lang(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    language = get_language(call.data)

    if language is not None:
        await state.update_data(language=language)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language['7'])

        if state == UserStates.Exist:
            msg = await bot.send_message(chat_id=call.message.chat.id, text=language['2'], reply_markup=add_comp(language['5'], language['11'], language['14']))
            await state.update_data(button=msg.message_id)
        elif state == UserStates.NotExist:
            msg = await bot.send_message(chat_id=call.message.chat.id, text=language['1'], reply_markup=share_keyboard)
            await state.update_data(lang_msg_id=msg.message_id)

@dp.message_handler(content_types=ContentType.CONTACT, state='*')
async def get_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    name = message.from_user.full_name
    user_id = message.from_user.id

    await state.update_data(userId=user_id)
    user.add(name, phone, user_id)

    temp_data = await state.get_data()
    message_id = temp_data.get('lang_msg_id')

    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    await bot.delete_message(chat_id=user_id, message_id=message_id)

    language = temp_data.get('language')
    msg = await bot.send_message(chat_id=message.chat.id, text=language['2'], reply_markup=add_comp(language['5'], language['11'], language['14']))
    await state.update_data(button=msg.message_id)


################################################################################

################################################################################


@dp.callback_query_handler(text="add", state='*')
async def message_handler(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await state.update_data(categoria=1)
    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    m = await bot.send_message(chat_id=call.message.chat.id, text=language['8'], reply_markup=no_photo(language['9'], language['12']))
    noPhotoButton = m.message_id
    await state.update_data(photoButton=noPhotoButton)
    await UserStates.Q6.set()

    @dp.callback_query_handler(text="enter", state='*')
    async def message_handler(call: CallbackQuery, state: FSMContext):
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        # await bot.send_photo(chat_id=call.message.chat.id, photo=open('instruction.jpg', 'rb'))
        await bot.send_message(chat_id=call.message.chat.id, text=language['13'])
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await UserStates.Q9.set()
        if categoria == 2:
            await UserStates.Q10.set()
        if categoria == 3:
            await UserStates.Q12.set()

    @dp.callback_query_handler(text="noPhoto", state='*')
    async def message_handler(call: CallbackQuery, state: FSMContext):
        await state.update_data(existPhoto=0)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language['3'])
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await UserStates.Q4.set()
        if categoria == 2:
            await UserStates.Q8.set()
        if categoria == 3:
            await UserStates.Q13.set()


@dp.message_handler(state=UserStates.Q9)
async def enter(message: Message, state: FSMContext):
    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']
    s = message.text

    region = atm.read(str(s))['State']

    if len(region) != 0:
        await state.update_data(existPhoto=1)
        await state.update_data(serialNum=s)
        await bot.send_message(chat_id=message.chat.id, text=language['3'])
        await UserStates.Q4.set()
    else:
        m = await bot.send_message(chat_id=message.chat.id, text=language['15'], reply_markup=no_photo(language['9'], language['12']))
        noPhotoButton = m.message_id
        await state.update_data(photoButton=noPhotoButton)
        await UserStates.Q6.set()


@dp.message_handler(content_types=ContentType.PHOTO, state=UserStates.Q6)
async def get_photo(message: Message, state: FSMContext):

    await message.photo[-1].download('qrcode.jpg')

    imgQRcode = cv2.imread('qrcode.jpg')
    code = decode(imgQRcode)

    for barcode in decode(imgQRcode):
        data = barcode.data.decode('utf-8')

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

        await bot.send_message(chat_id=message.chat.id, text=language['3'])
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await UserStates.Q4.set()
        if categoria == 2:
            await UserStates.Q8.set()
        if categoria == 3:
            await UserStates.Q13.set()

    else:

        tempForLanguage = await state.get_data('language')
        language = tempForLanguage['language']

        temp = await state.get_data('photoButton')
        messegeId = temp['photoButton']

        await bot.edit_message_text(chat_id=message.chat.id, message_id=messegeId, text=language['8'])

        m = await bot.send_message(chat_id=message.chat.id, text=language['10'], reply_markup=no_photo(language['9'], language['12']))
        noPhotoButton = m.message_id
        await state.update_data(photoButton=noPhotoButton)
        await UserStates.Q6.set()

        @dp.callback_query_handler(text="enter", state='*')
        async def message_handler(call: CallbackQuery, state: FSMContext):
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await bot.send_message(chat_id=call.message.chat.id, text=language['13'])
            tempCategoria = await state.get_data('categoria')
            categoria = tempCategoria['categoria']
            if categoria == 1:
                await UserStates.Q9.set()
            if categoria == 2:
                await UserStates.Q10.set()
            if categoria == 3:
                await UserStates.Q12.set()

        @dp.callback_query_handler(text="noPhoto", state='*')
        async def message_handler(call: CallbackQuery, state: FSMContext):
            await state.update_data(existPhoto=0)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language['3'])
            tempCategoria = await state.get_data('categoria')
            categoria = tempCategoria['categoria']
            if categoria == 1:
                await UserStates.Q4.set()
            if categoria == 2:
                await UserStates.Q8.set()
            if categoria == 3:
                await UserStates.Q13.set()


@dp.message_handler(state=UserStates.Q4)
async def Complaint(message: Message, state: FSMContext):
    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']

    uinfo = user.info(message.chat.id)

    com1 = message.text

    com = com1.replace("'", "''")

    currentHour = datetime.now().hour

    currentDay = datetime.now().weekday()

    tempExistPhoto = await state.get_data('existPhoto')
    existPhoto = tempExistPhoto['existPhoto']

    if currentHour < 9 or currentHour >= 18 or currentDay > 5:
        await bot.send_message(message.chat.id, language['6'], reply_markup=add_comp(language['5'], language['11'], language['14']))
    else:
        await bot.send_message(message.chat.id, language['4'], reply_markup=add_comp(language['5'], language['11'], language['14']))

    for x in cart:
        result1 = re.findall(x, com)

    for x in cashout:
        result2 = re.findall(x, com)

    for x in exchange:
        result3 = re.findall(x, com)

    cats = []
    if len(result1) != 0:
        cats.append('cart')
    if len(result2) != 0:
        cats.append('cashout')
    if len(result3) != 0:
        cats.append('exchange')

    userid = message.from_user.id

    if existPhoto == 0:

        await bot.send_message(chat_id=GROUP_ID, text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + message.text)

        if len(cats) == 1:
            ticket.add_status(userid, com, cats[0], '-')

        if len(cats) == 2:
            tempStr = cats[0]+','+cats[1]
            ticket.add_status(userid, com, tempStr, '-')

        if len(cats) == 3:
            tempStr = cats[0]+','+cats[1]+','+cats[2]
            ticket.add_status(userid, com, tempStr, '-')

        if len(cats) == 0:
            ticket.add_status(userid, com, 'other', '-')

    if existPhoto == 1:
        tempSerialNum = await state.get_data('serialNum')
        serialNum = tempSerialNum['serialNum']

        atm_data = atm.read(str(serialNum))
        region = atm_data['State']
        TerminalID = atm_data['TerminalID']
        Location = atm_data['Location']

        await bot.send_message(chat_id=GROUP_ID, text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + '<b>' + 'Region: ' + str(region[0]) + '\n' + 'Terminal ID: ' + str(TerminalID[0]) + '\n' + 'Location: ' + str(Location[0]) + '</b>' + '\n' + message.text)

        chatId = user.admin_by_state(str(region[0]))

        for i in chatId:
            await bot.send_message(chat_id=str(i[0]), text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + '<b>' + 'Region: ' + str(region[0]) + '\n' + 'Terminal ID: ' + str(TerminalID[0]) + '\n' + 'Location: ' + str(Location[0]) + '</b>' + '\n' + message.text)

        if len(cats) == 1:
            ticket.add_status(userid, com, cats[0], serialNum)

        if len(cats) == 2:
            tempStr = cats[0]+','+cats[1]
            ticket.add_status(userid, com, tempStr, serialNum)

        if len(cats) == 3:
            tempStr = cats[0]+','+cats[1]+','+cats[2]
            ticket.add_status(userid, com, tempStr, serialNum)

        if len(cats) == 0:
            ticket.add_status(userid, com, 'other', serialNum)


@dp.callback_query_handler(text="card", state='*')
async def message_handler(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await state.update_data(categoria=2)
    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    m = await bot.send_message(chat_id=call.message.chat.id, text=language['8'], reply_markup=no_photo(language['9'], language['12']))
    noPhotoButton = m.message_id
    await state.update_data(photoButton=noPhotoButton)
    await UserStates.Q7.set()

    @dp.callback_query_handler(text="enter", state='*')
    async def message_handler(call: CallbackQuery, state: FSMContext):
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id, text=language['13'])
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await UserStates.Q9.set()
        if categoria == 2:
            await UserStates.Q10.set()
        if categoria == 3:
            await UserStates.Q12.set()

    @dp.callback_query_handler(text="noPhoto", state='*')
    async def message_handler(call: CallbackQuery, state: FSMContext):
        await state.update_data(existPhoto=0)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language['3'])
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await UserStates.Q4.set()
        if categoria == 2:
            await UserStates.Q8.set()
        if categoria == 3:
            await UserStates.Q13.set()


@dp.message_handler(state=UserStates.Q10)
async def enter(message: Message, state: FSMContext):
    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']
    s = message.text

    atm_data = atm.read(str(s))
    region = atm_data['State']

    if len(region) != 0:
        await state.update_data(existPhoto=1)
        await state.update_data(serialNum=s)
        await bot.send_message(chat_id=message.chat.id, text=language['3'])
        await UserStates.Q8.set()
    else:
        m = await bot.send_message(chat_id=message.chat.id, text=language['15'], reply_markup=no_photo(language['9'], language['12']))
        noPhotoButton = m.message_id
        await state.update_data(photoButton=noPhotoButton)
        await UserStates.Q7.set()


@dp.message_handler(content_types=ContentType.PHOTO, state=UserStates.Q7)
async def get_photo(message: Message, state: FSMContext):

    await message.photo[-1].download('qrcode.jpg')

    imgQRcode = cv2.imread('qrcode.jpg')
    code = decode(imgQRcode)

    for barcode in decode(imgQRcode):
        data = barcode.data.decode('utf-8')

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

        await bot.send_message(chat_id=message.chat.id, text=language['3'])
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await UserStates.Q4.set()
        if categoria == 2:
            await UserStates.Q8.set()
        if categoria == 3:
            await UserStates.Q13.set()

    else:

        tempForLanguage = await state.get_data('language')
        language = tempForLanguage['language']

        temp = await state.get_data('photoButton')
        messegeId = temp['photoButton']

        await bot.edit_message_text(chat_id=message.chat.id, message_id=messegeId, text=language['8'])

        m = await bot.send_message(chat_id=message.chat.id, text=language['10'], reply_markup=no_photo(language['9'], language['12']))
        noPhotoButton = m.message_id
        await state.update_data(photoButton=noPhotoButton)
        await UserStates.Q6.set()

        @dp.callback_query_handler(text="enter", state='*')
        async def message_handler(call: CallbackQuery, state: FSMContext):
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await bot.send_message(chat_id=call.message.chat.id, text=language['13'])
            tempCategoria = await state.get_data('categoria')
            categoria = tempCategoria['categoria']
            if categoria == 1:
                await UserStates.Q9.set()
            if categoria == 2:
                await UserStates.Q10.set()
            if categoria == 3:
                await UserStates.Q12.set()

        @dp.callback_query_handler(text="noPhoto", state='*')
        async def message_handler(call: CallbackQuery, state: FSMContext):
            await state.update_data(existPhoto=0)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language['3'])
            tempCategoria = await state.get_data('categoria')
            categoria = tempCategoria['categoria']
            if categoria == 1:
                await UserStates.Q4.set()
            if categoria == 2:
                await UserStates.Q8.set()
            if categoria == 3:
                await UserStates.Q13.set()


@dp.message_handler(state=UserStates.Q8)
async def Complaint(message: Message, state: FSMContext):
    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']
    uinfo = user.info(message.chat.id)

    com1 = message.text

    com = com1.replace("'", "''")

    currentHour = datetime.now().hour

    currentDay = datetime.now().weekday()

    tempExistPhoto = await state.get_data('existPhoto')
    existPhoto = tempExistPhoto['existPhoto']

    if currentHour < 9 or currentHour >= 18 or currentDay > 5:
        await bot.send_message(message.chat.id, language['6'], reply_markup=add_comp(language['5'], language['11'], language['14']))
    else:
        await bot.send_message(message.chat.id, language['4'], reply_markup=add_comp(language['5'], language['11'], language['14']))

    userid = message.from_user.id

    if existPhoto == 0:

        await bot.send_message(chat_id=GROUP_ID, text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + message.text)
        ticket.add_status(userid, com, "card", '-')

    if existPhoto == 1:

        tempSerialNum = await state.get_data('serialNum')
        serialNum = tempSerialNum['serialNum']

        atm_data = atm.read(str(s))
        region = atm_data['State']
        TerminalID = atm_data['TerminalID']
        Location = atm_data['Location']

        await bot.send_message(chat_id=GROUP_ID, text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + '<b>' + 'Region: ' + str(region[0]) + '\n' + 'Terminal ID: ' + str(TerminalID[0]) + '\n' + 'Location: ' + str(Location[0]) + '</b>' + '\n' + message.text)

        chatId = user.admin_by_state(str(region[0]))

        for i in chatId:
            await bot.send_message(chat_id=str(i[0]), text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + '<b>' + 'Region: ' + str(region[0]) + '\n' + 'Terminal ID: ' + str(TerminalID[0]) + '\n' + 'Location: ' + str(Location[0]) + '</b>' + '\n' + message.text)

        tempSerialNum = await state.get_data('serialNum')
        serialNum = tempSerialNum['serialNum']
        ticket.add_status(userid, com, "card", serialNum)


@dp.callback_query_handler(text="cashout", state='*')
async def message_handler(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')

    await state.update_data(categoria=3)

    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    m = await bot.send_message(chat_id=call.message.chat.id, text=language['8'], reply_markup=no_photo(language['9'], language['12']))
    noPhotoButton = m.message_id
    await state.update_data(photoButton=noPhotoButton)
    await UserStates.Q11.set()

    @dp.callback_query_handler(text="enter", state='*')
    async def message_handler(call: CallbackQuery, state: FSMContext):
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        # await bot.send_photo(chat_id=call.message.chat.id, photo=open('instruction.jpg', 'rb'))
        await bot.send_message(chat_id=call.message.chat.id, text=language['13'])
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await UserStates.Q9.set()
        if categoria == 2:
            await UserStates.Q10.set()
        if categoria == 3:
            await UserStates.Q12.set()

    @dp.callback_query_handler(text="noPhoto", state='*')
    async def message_handler(call: CallbackQuery, state: FSMContext):
        await state.update_data(existPhoto=0)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language['3'])
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await UserStates.Q4.set()
        if categoria == 2:
            await UserStates.Q8.set()
        if categoria == 3:
            await UserStates.Q13.set()


@dp.message_handler(state=UserStates.Q12)
async def enter(message: Message, state: FSMContext):
    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']
    s = message.text

    atm_data = atm.read(str(s))
    region = atm_data['State']

    if len(region) != 0:
        await state.update_data(existPhoto=1)
        await state.update_data(serialNum=s)
        await bot.send_message(chat_id=message.chat.id, text=language['3'])
        await UserStates.Q13.set()
    else:
        m = await bot.send_message(chat_id=message.chat.id, text=language['15'], reply_markup=no_photo(language['9'], language['12']))
        noPhotoButton = m.message_id
        await state.update_data(photoButton=noPhotoButton)
        await UserStates.Q11.set()


@dp.message_handler(content_types=ContentType.PHOTO, state=UserStates.Q11)
async def get_photo(message: Message, state: FSMContext):

    await message.photo[-1].download('qrcode.jpg')

    imgQRcode = cv2.imread('qrcode.jpg')
    code = decode(imgQRcode)

    for barcode in decode(imgQRcode):
        data = barcode.data.decode('utf-8')

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

        await bot.send_message(chat_id=message.chat.id, text=language['3'])
        tempCategoria = await state.get_data('categoria')
        categoria = tempCategoria['categoria']
        if categoria == 1:
            await UserStates.Q4.set()
        if categoria == 2:
            await UserStates.Q8.set()
        if categoria == 3:
            await UserStates.Q13.set()

    else:

        tempForLanguage = await state.get_data('language')
        language = tempForLanguage['language']

        temp = await state.get_data('photoButton')
        messegeId = temp['photoButton']

        await bot.edit_message_text(chat_id=message.chat.id, message_id=messegeId, text=language['8'])

        m = await bot.send_message(chat_id=message.chat.id, text=language['10'], reply_markup=no_photo(language['9'], language['12']))
        noPhotoButton = m.message_id
        await state.update_data(photoButton=noPhotoButton)
        await UserStates.Q6.set()

        @dp.callback_query_handler(text="enter", state='*')
        async def message_handler(call: CallbackQuery, state: FSMContext):
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            # await bot.send_photo(chat_id=call.message.chat.id, photo=open('instruction.jpg', 'rb'))
            await bot.send_message(chat_id=call.message.chat.id, text=language['13'])
            tempCategoria = await state.get_data('categoria')
            categoria = tempCategoria['categoria']
            if categoria == 1:
                await UserStates.Q9.set()
            if categoria == 2:
                await UserStates.Q10.set()
            if categoria == 3:
                await UserStates.Q12.set()

        @dp.callback_query_handler(text="noPhoto", state='*')
        async def message_handler(call: CallbackQuery, state: FSMContext):
            await state.update_data(existPhoto=0)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language['3'])
            tempCategoria = await state.get_data('categoria')
            categoria = tempCategoria['categoria']
            if categoria == 1:
                await UserStates.Q4.set()
            if categoria == 2:
                await UserStates.Q8.set()
            if categoria == 3:
                await UserStates.Q13.set()


@dp.message_handler(state=UserStates.Q13)
async def Complaint(message: Message, state: FSMContext):
    tempForLanguage = await state.get_data('language')
    language = tempForLanguage['language']
    uinfo = user.info(message.chat.id)

    com1 = message.text

    com = com1.replace("'", "''")

    currentHour = datetime.now().hour

    currentDay = datetime.now().weekday()

    tempExistPhoto = await state.get_data('existPhoto')
    existPhoto = tempExistPhoto['existPhoto']

    if currentHour < 9 or currentHour >= 18 or currentDay > 5:
        await bot.send_message(message.chat.id, language['6'], reply_markup=add_comp(language['5'], language['11'], language['14']))
    else:
        await bot.send_message(message.chat.id, language['4'], reply_markup=add_comp(language['5'], language['11'], language['14']))

    userid = message.from_user.id

    if existPhoto == 0:

        await bot.send_message(chat_id=GROUP_ID, text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + message.text)
        ticket.add_status(userid, com, "cashout", '-')

    if existPhoto == 1:

        tempSerialNum = await state.get_data('serialNum')
        serialNum = tempSerialNum['serialNum']

        atm_data = atm.read(str(serialNum))
        region = atm_data['State']
        TerminalID = atm_data['TerminalID']
        Location = atm_data['Location']

        await bot.send_message(chat_id=GROUP_ID, text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + '<b>' + 'Region: ' + str(region[0]) + '\n' + 'Terminal ID: ' + str(TerminalID[0]) + '\n' + 'Location: ' + str(Location[0]) + '</b>' + '\n' + message.text)

        chatId = user.admin_by_state(str(region[0]))

        for i in chatId:
            await bot.send_message(chat_id=str(i[0]), text='<b>' + str(uinfo[0]) + '</b> (' + uinfo[1] + ')' + '\n' + '<b>' + 'Region: ' + str(region[0]) + '\n' + 'Terminal ID: ' + str(TerminalID[0]) + '\n' + 'Location: ' + str(Location[0]) + '</b>' + '\n' + message.text)

        tempSerialNum = await state.get_data('serialNum')
        serialNum = tempSerialNum['serialNum']
        ticket.add_status(userid, com, "cashout", serialNum)


@dp.message_handler(content_types=ContentType.ANY, state='*')
async def Complaint(message: Message):
    if message.chat.id != GROUP_ID:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
