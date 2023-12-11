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
    ticket_id = ticket.get_last_num_card_reissue()
    ticket_id = int(ticket_id) + 1

    url = "https://185.217.131.28:7000/feedback/"

    # feedback_data = {
    #     "type": "TRANSFER",
    #     "user_id": str(user_id),
    #     "client_form": com,
    #     "category": "Другое",
    #     "device_uid": '-' if exist_photo == 0 else str(serial_num),
    # }

    # async with httpx.AsyncClient() as client:
    #     response = await client.post(url, json=feedback_data)

    ticket.add_ticket_card_reissue(user_id, card_reissue_ticket, 'card_reissue')
    card_reissue_ticket = "Заявка на перевод карты от " + '<b>' + str(uinfoCut[0]) + '</b> \nФорма составленная клиентом: \n------------------\n' + card_reissue_ticket + '\n------------------\n' + "Номер телефона: <b>(" + uinfoCut[1] + ") </b>"
    card_reissue_ticket = str(ticket_id) + '\n' + card_reissue_ticket
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
