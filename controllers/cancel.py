import configparser

from dispatcher import dp
from states import UserStates

from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, CallbackQuery, Message

import services.methods.cancellation_the_transaction as cancellation_the_transaction

# database
config_file = 'config.ini'

# config.ini
config = configparser.ConfigParser()
config.read(config_file)
GROUP_ID = config.get('bot', 'group_id')
FILIAL = config.get('bot', 'filial')
TOKEN = config.get('bot', 'token')

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