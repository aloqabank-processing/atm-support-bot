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
import services.methods.atm_repair as atm_repair

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
# List of ATM models
atm_model_array = ["C2040", "C2060", "C2070", "C4060", "DN200H", "GRG H22", "GRG H68NL", "GRG H68VL", "GRG P5800VL", "NCR 6622", "NCR 6623", "NCR 6682"]
# List of terminal id
terminal_id_array = atm_repair.just_to_get_terminal_id_list()

# # # # # # # # # # # # # # # # # #
# Registration and Auth
# # # # # # # # # # # # # # # # # #
# Press /start to pay.. to start I mean. Cheking what type of user pressed /start (authorized or not)
@dp.message_handler(commands="start", state='*')
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    chat_id = message.chat.id
    await language_select.admin_exist(user_id, chat_id, message, state)
# Language select
@dp.callback_query_handler( text= ["Ru","Uz"] ,state=[UserStates.Exist, UserStates.NotExist])
async def select_lang(call: CallbackQuery, state: FSMContext):
    await call.answer('Done') 
    await language_select.select_language(FILIAL, call, state)
# Registration if user is unauthorized
@dp.message_handler(content_types=ContentType.CONTACT, state='*')
async def get_contact(message: Message, state: FSMContext):
    await language_select.registation(GROUP_ID, message, state)

# # # # # # # # # # # # # # # # # #
# Main menu
# # # # # # # # # # # # # # # # # #
# Choose problem or ticket 
@dp.callback_query_handler(text=["card_reissue", "ATM", "tickets", "cancellation_the_transaction", "atm_repair"], state='*')
async def choose_problem_async(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await main_menu.main_menu(call, state)
# Ticket-Callback catcher (to list all user tickets)
@dp.callback_query_handler(lambda query: re.match(r'^\d+$', query.data), state='*')
async def ticket_menu(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await main_menu.ticket_menu(call, state)
# Intermediate Stage after user submit ticket
@dp.callback_query_handler(text='cont', state='*')
async def next(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await main_menu.next(FILIAL, call, state)

# # # # # # # # # # # # # # # # # #
# ATM repair
# # # # # # # # # # # # # # # # # #
# Getting ATM-model by state
@dp.callback_query_handler(text=["Amaliyot", "Qoraqalpogiston", "Xorazm", "Namangan", "Andijon", "Buxoro", "Surxondaryo", "Samarqand", "Qashqadaryo", "Navoiy", "Fargona", "Jizzax", "Qoqon"], state='*')
async def model_by_filial(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await atm_repair.model_by_filial(call, state)
# Getting terminal ID by ATM-model
@dp.callback_query_handler(text=atm_model_array, state='*')
async def terminal_id_by_model(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await atm_repair.terminal_id_by_model(call, state)
# Asking for a form by terminal id
@dp.callback_query_handler(text=terminal_id_array, state='*')
async def ask_form(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await atm_repair.ask_form(call, state)
# Filling form for ATM repair ticket
@dp.message_handler(content_types=ContentType.TEXT, state=UserStates.atm_repair_get_form)
async def get_form(message: Message, state: FSMContext):
    await atm_repair.get_form(GROUP_ID, message, state)
# Something like admin panel in admin group to operate with tickets
@dp.callback_query_handler(text=["answer_ticket_atm_repair", "status_ticket_atm_repair", "close_ticket_atm_repair"], state='*')
async def admin_operations(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await atm_repair.admin_operations(GROUP_ID, call, state)
# Action to change status
@dp.message_handler(chat_id=GROUP_ID, state=UserStates.admin_group_status_cancellation_the_transaction)
async def change_status(message: Message, state: FSMContext):
    await atm_repair.change_status(GROUP_ID, message, state)
# Action to change answer
@dp.message_handler(chat_id=GROUP_ID, state=UserStates.admin_group_answer_cancellation_the_transaction)
async def change_answer(message: Message, state: FSMContext):
    await atm_repair.change_answer(GROUP_ID, message, state)

# # # # # # # # # # # # # # # # # #
# Cancellation The Transaction
# # # # # # # # # # # # # # # # # #
# There are 2 different tickets for HUMO and UZCARD. They differ in form
@dp.callback_query_handler(text=["HUMO", "UZCARD"], state='*')
async def choose_payment_method(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await cancellation_the_transaction.choose_payment_method(call, state)
# Form for UZCARD
@dp.message_handler(content_types=ContentType.TEXT, state=UserStates.cancellation_the_transaction_state_uzcard)
async def uzcard(message: Message, state: FSMContext):
    await cancellation_the_transaction.uzcard(GROUP_ID, message, state)
# Form for HUMO
@dp.message_handler(content_types=ContentType.DOCUMENT, state=UserStates.cancellation_the_transaction_state)
async def humo(message: Message, state: FSMContext):
    await cancellation_the_transaction.humo(GROUP_ID, message, state)
# Something like admin panel in admin group to operate with tickets
@dp.callback_query_handler(text=["close_ticket_cancellation_the_transaction_state", "answer_ticket_cancellation_the_transaction_state", "status_ticket_cancellation_the_transaction_state"], state='*')
async def admin_operations(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await cancellation_the_transaction.admin_operations(GROUP_ID, call, state)
# Action to change status
@dp.message_handler(chat_id=GROUP_ID, state=UserStates.admin_group_status_cancellation_the_transaction)
async def change_status(message: Message, state: FSMContext):
    await cancellation_the_transaction.change_status(GROUP_ID, message, state)
# Action to change answer
@dp.message_handler(chat_id=GROUP_ID, state=UserStates.admin_group_answer_cancellation_the_transaction)
async def change_answer(message: Message, state: FSMContext):
    await cancellation_the_transaction.change_answer(GROUP_ID, message, state)

# # # # # # # # # # # # # # # # # #
# Card Reissue
# # # # # # # # # # # # # # # # # #
# Text catcher to get filled form 
@dp.message_handler(content_types=ContentType.TEXT, state=UserStates.card_reissue)
async def get_form(message: Message, state: FSMContext):
    await card_reissue.get_form(GROUP_ID, message, state)
# Something like admin panel in admin group to operate with tickets
@dp.callback_query_handler(text=["close_ticket_card_reissue", "answer_ticket_card_reissue", "status_ticket_card_reissue"], state='*')
async def admin_operations(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await card_reissue.admin_operations(GROUP_ID, call, state)
# Action to change status
@dp.message_handler(chat_id=GROUP_ID, state=UserStates.admin_group_status)
async def change_status(message: Message, state: FSMContext):
    await card_reissue.change_status(GROUP_ID, message, state)
# Action to change answer
@dp.message_handler(chat_id=GROUP_ID, state=UserStates.admin_group_answer)
async def change_answer(message: Message, state: FSMContext):
    await card_reissue.change_answer(GROUP_ID, message, state)

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

# # # # # # # # # # # # # # # # # #
# Garbage Handler
# # # # # # # # # # # # # # # # # #
# Puts things in order in the chat
@dp.message_handler(content_types=ContentType.ANY, state='*')
async def chat_free(message: Message):
    if message.chat.id != GROUP_ID:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

# END
