import configparser

from dispatcher import dp
from states import UserStates

from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, CallbackQuery, Message

import services.methods.card_reissue as card_reissue

# database
config_file = 'config.ini'

# config.ini
config = configparser.ConfigParser()
config.read(config_file)
GROUP_ID = config.get('bot', 'group_id')
FILIAL = config.get('bot', 'filial')
TOKEN = config.get('bot', 'token')


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