import re
import configparser
import logging

from dispatcher import bot, dp
from states import UserStates

from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, CallbackQuery, Message

import services.language_select as language_select
import services.main_menu as main_menu
import services.methods.cancellation_the_transaction as cancellation_the_transaction
import services.methods.card_reissue as card_reissue
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

# Configure logging
logging.basicConfig(level=logging.INFO)

# # # # # # # # # # # # # # # # # #
# Registration and Auth
# # # # # # # # # # # # # # # # # #

@dp.message_handler(commands="start", state='*')
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    chat_id = message.chat.id
    await language_select.admin_exist(user_id, chat_id, message, state)

@dp.callback_query_handler( text= ["Ru","Uz"] ,state=[UserStates.Exist, UserStates.NotExist])
async def select_lang(call: CallbackQuery, state: FSMContext):
    await call.answer('Done') 
    await language_select.select_language(FILIAL, call, state)

@dp.message_handler(content_types=ContentType.CONTACT, state='*')
async def get_contact(message: Message, state: FSMContext):
    await language_select.registation(GROUP_ID, message, state)

@dp.callback_query_handler(text=["card_reissue", "ATM", "tickets", "cancellation_the_transaction"], state='*')
async def choose_problem_async(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await main_menu.main_menu(call, state)

@dp.callback_query_handler(text=["HUMO", "UZCARD"], state='*')
async def choose_problem_async(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await cancellation_the_transaction.choose_payment_method(call, state)

@dp.callback_query_handler(lambda query: re.match(r'^\d+$', query.data), state='*')
async def process_callback_number(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await main_menu.ticket_menu(call, state)
 
@dp.message_handler(content_types=ContentType.TEXT, state=UserStates.cancellation_the_transaction_state_uzcard)
async def cancellation_the_transaction_uzcard(message: Message, state: FSMContext):
    await cancellation_the_transaction.uzcard(GROUP_ID, message, state)

@dp.message_handler(content_types=ContentType.DOCUMENT, state=UserStates.cancellation_the_transaction_state)
async def cancellation_the_transaction_func(message: Message, state: FSMContext):
    await cancellation_the_transaction.humo(GROUP_ID, message, state)

@dp.callback_query_handler(text=["close_ticket_cancellation_the_transaction_state", "answer_ticket_cancellation_the_transaction_state", "status_ticket_cancellation_the_transaction_state"], state='*')
async def close_ticket_card_reissue_func(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await cancellation_the_transaction.admin_operations(GROUP_ID, call, state)

@dp.message_handler(chat_id=GROUP_ID, state=UserStates.admin_group_status_cancellation_the_transaction)
async def enter(message: Message, state: FSMContext):
    await cancellation_the_transaction.change_status(GROUP_ID, message, state)
    
@dp.message_handler(chat_id=GROUP_ID, state=UserStates.admin_group_answer_cancellation_the_transaction)
async def enter(message: Message, state: FSMContext):
    await cancellation_the_transaction.change_answer(GROUP_ID, message, state)

@dp.message_handler(content_types=ContentType.TEXT, state=UserStates.card_reissue)
async def get_card_reissue(message: Message, state: FSMContext):
    await card_reissue.get_form(GROUP_ID, message, state)

@dp.callback_query_handler(text=["close_ticket_card_reissue", "answer_ticket_card_reissue", "status_ticket_card_reissue"], state='*')
async def close_ticket_card_reissue_func(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await card_reissue.admin_operations(GROUP_ID, call, state)
    
@dp.message_handler(chat_id=GROUP_ID, state=UserStates.admin_group_status)
async def enter(message: Message, state: FSMContext):
    await card_reissue.change_status(GROUP_ID, message, state)
    
@dp.message_handler(chat_id=GROUP_ID, state=UserStates.admin_group_answer)
async def enter(message: Message, state: FSMContext):
    await card_reissue.change_answer(GROUP_ID, message, state)

# # # # # # # # # # # # # # # # # #
# ?
# # # # # # # # # # # # # # # # # #

@dp.callback_query_handler(text=["add", "cashout", "card"], state='*')
async def choose_device(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await atm_servise.choose_category(call, state)

@dp.callback_query_handler(text=["location", "QR", "back_from_choose_ATM"], state='*')
async def choose_method(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await atm_servise.method_to_choose_atm(FILIAL, call, state)

@dp.message_handler(content_types=ContentType.LOCATION, state=UserStates.Location)
async def get_location(message: Message, state: FSMContext):
    await atm_methods.device_by_location(message, state)
    
@dp.callback_query_handler(text=["enter", "noPhoto"], state='*')
async def device_processing(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await atm_methods.qr_methods(call, state)

@dp.callback_query_handler(text='cont', state='*')
async def device_processing(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await main_menu.next(FILIAL, call, state)

@dp.message_handler(state=UserStates.Q9)
async def enter(message: Message, state: FSMContext):
    await atm_methods.no_photo_enter(message, state)

@dp.message_handler(content_types=ContentType.PHOTO, state=UserStates.Q6)
async def get_photo(message: Message, state: FSMContext):
    await atm_methods.device_by_qr(message, state)

@dp.message_handler(state=UserStates.Q4)
async def complaint(message: Message, state: FSMContext):
    await atm_servise.get_form(GROUP_ID, message, state)

@dp.callback_query_handler(text=["close_atm_ticket", "answer_atm_ticket", "status_atm_ticket"], state='*')
async def close_ticket_card_reissue_func(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await atm_servise.admin_operations(GROUP_ID, call, state)
    
@dp.message_handler(chat_id=GROUP_ID, state=UserStates.admin_group_ticket_status)
async def enter(message: Message, state: FSMContext):
    await atm_servise.change_status(GROUP_ID, message, state)
    
@dp.message_handler(chat_id=GROUP_ID, state=UserStates.admin_group_ticket_answer)
async def enter(message: Message, state: FSMContext):
    await atm_servise.change_answer(GROUP_ID, message, state)

# END

@dp.message_handler(content_types=ContentType.ANY, state='*')
async def chat_free(message: Message):
    if message.chat.id != GROUP_ID:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
