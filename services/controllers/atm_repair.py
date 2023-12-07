import configparser

from dispatcher import dp
from states import UserStates

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

import services.methods.atm_repair as atm_repair

# database
config_file = 'config.ini'

# config.ini
config = configparser.ConfigParser()
config.read(config_file)
GROUP_ID = config.get('bot', 'group_id')
FILIAL = config.get('bot', 'filial')
TOKEN = config.get('bot', 'token')

# List of ATM models
atm_model_array = ["C2040", "C2060", "C2070", "C4060", "DN200H", "GRG H22", "GRG H68NL", "GRG H68VL", "GRG P5800VL", "NCR 6622", "NCR 6623", "NCR 6682"]
# List of terminal id
terminal_id_array = atm_repair.just_to_get_terminal_id_list()
print(terminal_id_array)

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
    print('ask form')
    await atm_repair.ask_form(call, state)
    await UserStates.atm_repair_get_form.set()
# Filling form for ATM repair ticket
@dp.message_handler(state=UserStates.atm_repair_get_form)
async def get_form(message: Message, state: FSMContext):
    print("atm_repair_get_form")
    await atm_repair.get_form(GROUP_ID, message, state)
# Something like admin panel in admin group to operate with tickets
@dp.callback_query_handler(text=["answer_ticket_atm_repair", "status_ticket_atm_repair", "close_ticket_atm_repair"], state='*')
async def admin_operations(call: CallbackQuery, state: FSMContext):
    await call.answer('Done')
    await atm_repair.admin_operations(GROUP_ID, call, state)
# Action to change status
@dp.message_handler(chat_id=GROUP_ID, state=UserStates.admin_group_status_atm_repair)
async def change_status(message: Message, state: FSMContext):
    await atm_repair.change_status(GROUP_ID, message, state)
# Action to change answer
@dp.message_handler(chat_id=GROUP_ID, state=UserStates.admin_group_answer_atm_repair)
async def change_answer(message: Message, state: FSMContext):
    await atm_repair.change_answer(GROUP_ID, message, state)