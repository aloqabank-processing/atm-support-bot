from dispatcher import bot
import keyboards as keyboard
from states import UserStates
from datetime import datetime
from repository import Ticket, User, Atm
from db import Database
import httpx
from api_query import FeedbackModule, AdministrationModule

config_file = 'config.ini'
db = Database(config_file)
ticket = Ticket(db)
user = User(db)
atm = Atm(db)


async def choose_category(call, state):
    if call.data == "add":
        await state.update_data(category=1)
    elif call.data == "cashout":
        await state.update_data(category=3)
    else:
        await state.update_data(category=2)
    temp_data = await state.get_data()
    language = temp_data.get('language')
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id, text=language['21'], reply_markup=keyboard.method_to_choose_ATM(language['22'], language['23'], language['24']))

async def method_to_choose_atm(FILIAL, call, state):
    temp_data = await state.get_data()
    language = temp_data.get('language')
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if call.data == "location":
        await bot.send_message(chat_id=call.message.chat.id, text=language['25'], reply_markup=keyboard.send_location(language['26']))
        await UserStates.Location.set()
    elif call.data == "QR":
        file2 = open('instruction.MP4', 'rb')
        msg = await bot.send_animation( chat_id=call.message.chat.id, animation= file2, caption=language['8'], reply_markup=keyboard.no_photo(language['9'], language['12']))
        await state.update_data(no_photo_button_message_id=msg.message_id)
        await UserStates.Q6.set()
    else:
        if str(call.message.chat.id) == FILIAL:
            await bot.send_message(chat_id=call.message.chat.id, text=language['20'], reply_markup=keyboard.choose_problem(language['18'], language['17'], language['19'], language['34'], language['39']))
        else:
            await bot.send_message(chat_id=call.message.chat.id, text=language['20'], reply_markup=keyboard.choose_problem_user(language['18'], language['17'], language['19']))

async def admin_operations(GROUP_ID, call, state):
    split_ticket_id = call.message.text
    split_ticket_id = split_ticket_id.split("\n")[0]
    await state.update_data(current_ticket=split_ticket_id)

    if call.data == "close_atm_ticket":
        await FeedbackModule.update_status(feedback_id=split_ticket_id, status="StatusType.CLOSED")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=GROUP_ID, text="Тикет №" + str(split_ticket_id) + " закрыт")
    elif call.data == "status_atm_ticket":
        current_ticket_text = call.message.text
        await state.update_data(current_ticket_text=current_ticket_text)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=GROUP_ID, text="Введите статус по данной заявке:")
        await UserStates.admin_group_ticket_status.set()
    elif call.data == "answer_atm_ticket":
        current_ticket_text = call.message.text
        await state.update_data(current_ticket_text=current_ticket_text)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=GROUP_ID, text="Введите свой ответ для клиента по данной заявке:")
        await UserStates.admin_group_ticket_answer.set()

async def change_status(GROUP_ID, message, state):
    status_by_admin = message.text
    temp_data = await state.get_data()
    current_ticket = temp_data.get('current_ticket')
    current_ticket_text = temp_data.get('current_ticket_text')

    await FeedbackModule.update_status(feedback_id=current_ticket, status=status_by_admin)

    await bot.send_message(chat_id=GROUP_ID, text="Статус заявки успешно обновлен!")
    await bot.send_message(chat_id=GROUP_ID, text=current_ticket_text, reply_markup=keyboard.options_atm_ticket() )
    await UserStates.wait.set()

async def change_answer(GROUP_ID, message, state):
    answer_by_admin = message.text
    temp_data = await state.get_data()
    current_ticket = temp_data.get('current_ticket')
    current_ticket_text = temp_data.get('current_ticket_text')

    await FeedbackModule.update_answer(answer_by_admin, current_ticket)

    await bot.send_message(chat_id=GROUP_ID, text="Ответ клиенту успешно добавлен!")
    await bot.send_message(chat_id=GROUP_ID, text=current_ticket_text, reply_markup=keyboard.options_atm_ticket() )
    await UserStates.wait.set()

async def get_form(GROUP_ID, message, state):
    temp_data = await state.get_data()
    language = temp_data.get('language')
    exist_photo = temp_data.get('exist_photo')
    serial_num = temp_data.get('serial_num')
    categoria = temp_data['category']

    user_id = message.from_user.id
    uinfo = await AdministrationModule.get_user(message.chat.id)
    uinfoCut = uinfo[0]
    com = message.text.replace("'", "''")

    current_hour = datetime.now().hour
    current_day = datetime.now().weekday()
    last_num = ticket.get_last_num()
    last_num = int(last_num) + 1

    if current_hour < 9 or current_hour >= 18 or current_day > 5:
        await bot.send_message(message.chat.id, str(last_num) + '\n' + language['6'], reply_markup=keyboard.Continue(language['16']))
    else:
        await bot.send_message(message.chat.id, str(last_num) + '\n' + language['4'], reply_markup=keyboard.Continue(language['16']))
    
    if categoria == 1:
        feedback_data = {
            "type": "ATM_FEEDBACK",
            "user_id": str(user_id),
            "client_form": com,
            "category": "Другое",
            "device_uid": '-' if exist_photo == 0 else str(serial_num),
        }
    elif categoria == 2:
        feedback_data = {
            "type": "ATM_FEEDBACK",
            "user_id": str(user_id),
            "client_form": com,
            "category": "Банкомат захватил карту",
            "device_uid": '-' if exist_photo == 0 else str(serial_num),
        }
    else:
        feedback_data = {
            "type": "ATM_FEEDBACK",
            "user_id": str(user_id),
            "client_form": com,
            "category": "Проблемы с выдачей наличных",
            "device_uid": '-' if exist_photo == 0 else str(serial_num),
        }

    await FeedbackModule.add_feedback(feedback_data)

    if exist_photo == 0:
        await bot.send_message(chat_id=GROUP_ID, text= str(last_num) + '\n' + '<b>' + str(uinfoCut['name']) + '</b> (' + uinfoCut['mobile'] + ')' + '\n' + message.text, reply_markup=keyboard.options_atm_ticket())
    else:
        atm_data = atm.read(str(serial_num))
        region = atm_data[0]
        TerminalID = atm_data[0]
        Location = atm_data[0]
        await bot.send_message(chat_id=GROUP_ID, text= str(last_num) + '\n' + '<b>' + str(uinfoCut['name']) + '</b> (' + uinfoCut['mobile'] + ')' + '\n' + '<b>' + 'Region: ' + str(region[1]) + '\n' + 'Terminal ID: ' + str(TerminalID[2]) + '\n' + 'Location: ' + str(Location[5]) + '</b>' + '\n' + message.text, reply_markup=keyboard.options_atm_ticket())
        chat_id = user.admin_by_state(str(region[1]))
        chat_idCut = chat_id[0]
        # for i in chat_idCut:
            # await bot.send_message(chat_id=str(i), text= str(last_num) + '\n' + '<b>' + str(uinfoCut[0]) + '</b> (' + uinfoCut[1] + ')' + '\n' + '<b>' + 'Region: ' + str(region[1]) + '\n' + 'Terminal ID: ' + str(TerminalID[2]) + '\n' + 'Location: ' + str(Location[5]) + '</b>' + '\n' + message.text, reply_markup=options_atm_ticket())