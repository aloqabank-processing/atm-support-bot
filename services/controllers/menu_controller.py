import re
import configparser

from dispatcher import bot, dp
from states import UserStates

from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, CallbackQuery, Message

import services.language_select as language_select
import services.main_menu as main_menu

# database
config_file = 'config.ini'

# config.ini
config = configparser.ConfigParser()
config.read(config_file)
GROUP_ID = config.get('bot', 'group_id')
FILIAL = config.get('bot', 'filial')
TOKEN = config.get('bot', 'token')

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
# Garbage Handler
# # # # # # # # # # # # # # # # # #
# Puts things in order in the chat
@dp.message_handler(content_types=ContentType.ANY, state='*')
async def chat_free(message: Message):
    if message.chat.id != GROUP_ID:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)