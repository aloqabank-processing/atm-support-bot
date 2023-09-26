from repository import Ticket, User
from db import Database
from dispatcher import bot
import keyboards as keyboard
from datetime import datetime
from states import UserStates

config_file = 'config.ini'
db = Database(config_file)
ticket = Ticket(db)
user = User(db)

async def get_form(GROUP_ID, message, state):
    card_reissue_ticket = message.text
    uinfo = user.info(message.from_user.id)
    uinfoCut = uinfo[0]

    temp_data = await state.get_data()
    language = temp_data.get('language')

    user_id = message.chat.id
    ticket.add_ticket_card_reissue(user_id, card_reissue_ticket, 'c')
    result = ticket.ticket_id_by_client_form(card_reissue_ticket)
    ticket_id = result[0]
    card_reissue_ticket = "Заявка на перевод карты от " + '<b>' + str(uinfoCut[0]) + '</b> \nФорма составленная клиентом: \n------------------\n' + card_reissue_ticket + '\n------------------\n' + "Номер телефона: <b>(" + uinfoCut[1] + ") </b>"
    card_reissue_ticket = str(ticket_id[0]) + '\n' + card_reissue_ticket
    await bot.send_message(chat_id=GROUP_ID, text=card_reissue_ticket, reply_markup=keyboard.options_ticket_card_reissue())
    
    current_hour = datetime.now().hour
    current_day = datetime.now().weekday()

    if current_hour < 9 or current_hour >= 18 or current_day > 5:
        await bot.send_message(message.chat.id, language['6'], reply_markup=keyboard.Continue(language['16']))
    else:
        await bot.send_message(message.chat.id, language['4'], reply_markup=keyboard.Continue(language['16']))

async def admin_operations(GROUP_ID, call, state):
    split_ticket_id = call.message.text
    split_ticket_id = split_ticket_id.split("\n")[0]
    await state.update_data(current_ticket=split_ticket_id)
    if call.data == "close_ticket_card_reissue":
        ticket.delete_ticket_card_reissue(split_ticket_id)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=GROUP_ID, text="Тикет №" + str(split_ticket_id) + " закрыт")
    elif call.data == "status_ticket_card_reissue":
        current_ticket_text = call.message.text
        await state.update_data(current_ticket_text=current_ticket_text)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=GROUP_ID, text="Введите статус по данной заявке:")
        await UserStates.admin_group_status.set()
    elif call.data == "answer_ticket_card_reissue":
        current_ticket_text = call.message.text
        await state.update_data(current_ticket_text=current_ticket_text)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=GROUP_ID, text="Введите свой ответ для клиента по данной заявке:")
        await UserStates.admin_group_answer.set()

async def change_status(GROUP_ID, message, state):
    status_by_admin = message.text
    temp_data = await state.get_data()
    current_ticket = temp_data.get('current_ticket')
    current_ticket_text = temp_data.get('current_ticket_text')

    ticket.update_status_by_id(status_by_admin, current_ticket)

    await bot.send_message(chat_id=GROUP_ID, text="Статус заявки успешно обновлен!")
    await bot.send_message(chat_id=GROUP_ID, text=current_ticket_text, reply_markup=keyboard.options_ticket_card_reissue() )
    await UserStates.wait.set()

async def change_answer(GROUP_ID, message, state):
    answer_by_admin = message.text
    temp_data = await state.get_data()
    current_ticket = temp_data.get('current_ticket')
    current_ticket_text = temp_data.get('current_ticket_text')

    ticket.update_answer_by_id(answer_by_admin, current_ticket)

    await bot.send_message(chat_id=GROUP_ID, text="Ответ клиенту успешно добавлен!")
    await bot.send_message(chat_id=GROUP_ID, text=current_ticket_text, reply_markup=keyboard.options_ticket_card_reissue() )
    await UserStates.wait.set()
