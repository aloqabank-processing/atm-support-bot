from dispatcher import bot
from states import UserStates
import keyboards as keyboard
import cv2
from pyzbar.pyzbar import decode
from geo import Distance
from repository import Atm
from db import Database

config_file = 'config.ini'
db = Database(config_file)
atm = Atm(db)
dis = Distance(db)

async def device_by_location(message, state):
    latitude = message.location.latitude
    longitude = message.location.longitude
    serial_num = dis.check_distance(longitude, latitude)
    
    temp_data = await state.get_data()
    language = temp_data.get('language')

    if serial_num != '0':
        unique_id = atm.unique_id_by_terminal(serial_num)[0]
        await state.update_data(exist_photo=1, serial_num=unique_id[0])
        await bot.send_message(chat_id=message.chat.id, text=language['3'])
        await UserStates.Q4.set()
    else:
        await bot.send_message(chat_id=message.chat.id, text=language['33'], reply_markup=keyboard.method_to_choose_ATM(language['22'], language['23'], language['24']))

async def qr_methods(call, state):
    temp_data = await state.get_data()
    language = temp_data.get('language')
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

async def no_photo_enter(message, state):
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
        msg = await bot.send_message(chat_id=message.chat.id, text=language['15'], reply_markup=keyboard.no_photo(language['9'], language['12']))
        await state.update_data(no_photo_button_message_id=msg.message_id)
        await UserStates.Q6.set()

async def device_by_qr(message, state):
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
    else:
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id)

        msg = await bot.send_message(chat_id=message.chat.id, text=language['10'], reply_markup=keyboard.no_photo(language['9'], language['12']))
        await state.update_data(no_photo_button_message_id=msg.message_id)
        await UserStates.Q6.set()