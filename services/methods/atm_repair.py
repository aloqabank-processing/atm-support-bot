from dispatcher import bot
from states import UserStates
import keyboards as keyboard
from repository import Atm, Ticket, User
from db import Database

config_file = 'config.ini'
db = Database(config_file)
atm = Atm(db)
ticket = Ticket(db)
user = User(db)

def just_to_get_terminal_id_list():
    terminal_id_list = atm.get_all_terminal_id()
    return terminal_id_list

async def model_by_filial(call, state):
    await state.update_data(atm_state=call.data)
    result = atm.get_model_by_filial( call.data )
    model = []
    for temp_model in result:
        model.append(temp_model[0])
    model = set(model)
    temp_data = await state.get_data()
    language = temp_data.get('language')
    await bot.send_message(chat_id=call.message.chat.id, text=language['41'], reply_markup=keyboard.model_list(model, language['24']))

async def terminal_id_by_model(call, state):
    temp_data = await state.get_data()
    language = temp_data.get('language')
    atm_state = temp_data.get('atm_state')
    terminal_id = atm.get_terminal_id_by_model(atm_state, call.data)
    await bot.send_message(chat_id=call.message.chat.id, text=language['42'], reply_markup=keyboard.terminal_id_list(terminal_id, language['24']))

async def ask_form(call, state):
    await state.update_data(terminal_id_for_atm_repair=call.data)
    temp_data = await state.get_data()
    language = temp_data.get('language')
    await bot.send_message(chat_id=call.message.chat.id, text=language['43'])
    await UserStates.atm_repair_get_form.set()

async def get_form(GROUP_ID, message, state):
    uinfo = user.info(message.from_user.id)
    uinfoCut = uinfo[0]
    temp_data = await state.get_data()
    language = temp_data.get('language')
    atm_state = temp_data.get('atm_state')
    terminal_id_for_atm_repair = temp_data.get('terminal_id_for_atm_repair')
    atm_repair_ticket = message.text.replace("'", "''")
    user_id = message.chat.id
    ticket_id = ticket.get_last_num_card_reissue()
    ticket_id = int(ticket_id) + 1

    ticket.add_ticket_card_reissue(user_id, atm_repair_ticket, terminal_id_for_atm_repair)
    ticket_form = "Заявка на починку банкомата от " + '<b>' + str(uinfoCut[0]) + "Регион: " + str(atm_state) + "\n" + "Terminal ID: " + str(terminal_id_for_atm_repair) + '</b>\nФорма составленная клиентом: \n------------------\n' + str(atm_repair_ticket) + '\n------------------\n' + "Номер телефона: <b>(" + uinfoCut[1] + ") </b>"
    ticket_form = str(ticket_id) + '\n' + ticket_form
    await bot.send_message(chat_id=GROUP_ID, text=ticket_form, reply_markup=keyboard.options_ticket_atm_repair())

async def admin_operations(GROUP_ID, call, state):
    split_ticket_id = call.message.text
    split_ticket_id = split_ticket_id.split("\n")[0]
    await state.update_data(current_ticket=split_ticket_id)
    if call.data == "close_ticket_atm_repair":
        ticket.delete_ticket_card_reissue(split_ticket_id)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=GROUP_ID, text="Тикет №" + str(split_ticket_id) + " закрыт")
    elif call.data == "status_ticket_atm_repair":
        current_ticket_text = call.message.text
        await state.update_data(current_ticket_text=current_ticket_text)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=GROUP_ID, text="Введите статус по данной заявке:")
        await UserStates.admin_group_status_atm_repair.set()
    elif call.data == "answer_ticket_atm_repair":
        current_ticket_text = call.message.text
        await state.update_data(current_ticket_text=current_ticket_text)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=GROUP_ID, text="Введите свой ответ для клиента по данной заявке:")
        await UserStates.admin_group_answer_atm_repair.set()

async def change_status(GROUP_ID, message, state):
    status_by_admin = message.text
    temp_data = await state.get_data()
    current_ticket = temp_data.get('current_ticket')
    current_ticket_text = temp_data.get('current_ticket_text')

    ticket.update_status_by_id(status_by_admin, current_ticket)

    await bot.send_message(chat_id=GROUP_ID, text="Статус заявки успешно обновлен!")
    await bot.send_message(chat_id=GROUP_ID, text=current_ticket_text, reply_markup=keyboard.options_ticket_atm_repair() )
    await UserStates.wait.set()

async def change_answer(GROUP_ID, message, state):
    answer_by_admin = message.text
    temp_data = await state.get_data()
    current_ticket = temp_data.get('current_ticket')
    current_ticket_text = temp_data.get('current_ticket_text')

    ticket.update_answer_by_id(answer_by_admin, current_ticket)

    await bot.send_message(chat_id=GROUP_ID, text="Ответ клиенту успешно добавлен!")
    await bot.send_message(chat_id=GROUP_ID, text=current_ticket_text, reply_markup=keyboard.options_ticket_atm_repair() )
    await UserStates.wait.set()

