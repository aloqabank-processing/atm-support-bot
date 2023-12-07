import configparser

from dispatcher import dp
from states import UserStates

from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, CallbackQuery, Message

import services.atm_servise as atm_servise
import services.methods.atm_methods as atm_methods

# database
config_file = 'config.ini'

# config.ini
config = configparser.ConfigParser()
config.read(config_file)
GROUP_ID = config.get('bot', 'group_id')
FILIAL = config.get('bot', 'filial')
TOKEN = config.get('bot', 'token')

# # # # # # # # # # # # # # # # # #
# ATM
# # # # # # # # # # # # # # # # # #
# What category client problem is
@dp.callback_query_handler(text=["add", "cashout", "card"], state='*')
async def choose_device(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await atm_servise.choose_category(call, state)
# Methods to identify ATM
@dp.callback_query_handler(text=["location", "QR", "back_from_choose_ATM"], state='*')
async def choose_method(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await atm_servise.method_to_choose_atm(FILIAL, call, state)
# Identify by location
@dp.message_handler(content_types=ContentType.LOCATION, state=UserStates.Location)
async def get_location(message: Message, state: FSMContext):
    await atm_methods.device_by_location(message, state)
# QR methods (is photo exist, enter serial manually or drop photo)
@dp.callback_query_handler(text=["enter", "noPhoto"], state='*')
async def qr_methods(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await atm_methods.qr_methods(call, state)
# Enter serial manually
@dp.message_handler(state=UserStates.Q9)
async def no_photo_enter(message: Message, state: FSMContext):
    await atm_methods.no_photo_enter(message, state)
# Decoding QR to get serial
@dp.message_handler(content_types=ContentType.PHOTO, state=UserStates.Q6)
async def get_photo(message: Message, state: FSMContext):
    await atm_methods.device_by_qr(message, state)
# Collecting all ticket data in 1 form
@dp.message_handler(state=UserStates.Q4)
async def get_form(message: Message, state: FSMContext):
    await atm_servise.get_form(GROUP_ID, message, state)
# Something like admin panel in admin group to operate with tickets
@dp.callback_query_handler(text=["close_atm_ticket", "answer_atm_ticket", "status_atm_ticket"], state='*')
async def admin_operations(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await atm_servise.admin_operations(GROUP_ID, call, state)
# Action to change status
@dp.message_handler(chat_id=GROUP_ID, state=UserStates.admin_group_ticket_status)
async def change_status(message: Message, state: FSMContext):
    await atm_servise.change_status(GROUP_ID, message, state)
# Action to change answer
@dp.message_handler(chat_id=GROUP_ID, state=UserStates.admin_group_ticket_answer)
async def change_answer(message: Message, state: FSMContext):
    await atm_servise.change_answer(GROUP_ID, message, state)