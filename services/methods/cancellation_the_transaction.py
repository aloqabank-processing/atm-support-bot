from dispatcher import bot
from states import UserStates
from repository import Ticket, User
from db import Database
import keyboards as keyboard
from api_query import FeedbackModule, AdministrationModule

config_file = 'config.ini'
db = Database(config_file)
ticket = Ticket(db)
user = User(db)

async def choose_payment_method(call, state):
    temp_data = await state.get_data()
    language = temp_data.get('language')
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if call.data == "HUMO":
        await bot.send_message(chat_id=call.message.chat.id, text=language['36'])
        await state.update_data(cancellation_the_transaction_type_state='HUMO')
        await UserStates.cancellation_the_transaction_state.set()
    else:
        await bot.send_message(chat_id=call.message.chat.id, text=language['38'])
        await state.update_data(cancellation_the_transaction_type_state='UZCARD')
        await UserStates.cancellation_the_transaction_state_uzcard.set()

async def uzcard(GROUP_ID, message, state):
    cancellation_the_transaction_text = message.text
    uinfo = user.info(message.from_user.id)
    uinfo = await AdministrationModule.get_user(message.from_user.id)
    uinfoCut = uinfo[0]

    temp_data = await state.get_data()
    language = temp_data.get('language')

    user_id = message.chat.id
    ticket.add_ticket_card_reissue(user_id, cancellation_the_transaction_text, 'UZCARD')

    params = {
        "type": "UZCARD",
        "user_id": uinfoCut['telegram_user_id'],
        "client_form": cancellation_the_transaction_text
    }
    await FeedbackModule.add_feedback(params)

    result = FeedbackModule.get_feedback_id_last(user_id)
    ticket_id = result['feedback_id']
    cancellation_the_transaction_text = "Заявка на отмену транзакции от " + '<b>' + str(uinfoCut['name']) + '</b> \nФорма составленная клиентом: \n------------------\n' + cancellation_the_transaction_text + '\n------------------\n' + "Номер телефона: <b>(" + uinfoCut['mobile'] + ") </b>"
    cancellation_the_transaction_text = str(ticket_id[0]) + '\n' + cancellation_the_transaction_text
    await bot.send_message(chat_id=GROUP_ID, text=cancellation_the_transaction_text, reply_markup=keyboard.options_ticket_card_reissue())
    await bot.send_message(message.chat.id, language['4'], reply_markup=keyboard.Continue(language['16']))

async def humo(GROUP_ID, message, state):
    file_info = message.document.file_id
    user_id = message.chat.id
    uinfo = user.info(message.from_user.id)
    temp_data = await state.get_data()
    language = temp_data.get('language')
    uinfoCut = uinfo[0]

    ticket_id = ticket.get_last_num_card_reissue()
    ticket_id = int(ticket_id) + 1
    ticket.add_ticket_card_reissue(user_id, file_info, 'cancellation_the_transaction')

    cancellation_the_transaction_ticket = "Заявка на отмену транзакции от " + '<b>' + str(uinfoCut[0]) + '</b> \nНомер телефона: <b>(' + uinfoCut[1] + ") </b>"
    cancellation_the_transaction_ticket = str(ticket_id) + '\n' + cancellation_the_transaction_ticket
    await bot.send_document(chat_id=GROUP_ID, document=file_info, caption=cancellation_the_transaction_ticket, reply_markup=keyboard.options_ticket_cancellation_the_transaction_state() )
    await bot.send_message(message.chat.id, language['4'], reply_markup=keyboard.Continue(language['16']))

async def change_status(GROUP_ID, message, state):
    status_by_admin = message.text
    temp_data = await state.get_data()
    current_ticket = temp_data.get('current_ticket')
    current_ticket_text = temp_data.get('current_ticket_text')

    result = ticket.file_id_by_ticket_id(current_ticket)[0]
    ticket_file_id = result[0]

    await FeedbackModule.update_status(feedback_id=current_ticket, status=status_by_admin)

    await bot.send_message(chat_id=GROUP_ID, text="Статус заявки успешно обновлен!")
    await bot.send_document(chat_id=GROUP_ID, document=str(ticket_file_id), caption=current_ticket_text, reply_markup=keyboard.options_ticket_cancellation_the_transaction_state() )
    await UserStates.wait.set()

async def change_answer(GROUP_ID, message, state):
    answer_by_admin = message.text
    temp_data = await state.get_data()
    current_ticket = temp_data.get('current_ticket')
    current_ticket_text = temp_data.get('current_ticket_text')

    result = ticket.file_id_by_ticket_id(current_ticket)[0]
    ticket_file_id = result[0]

    await FeedbackModule.update_answer(answer_by_admin, current_ticket)

    await bot.send_message(chat_id=GROUP_ID, text="Ответ клиенту успешно добавлен!")
    await bot.send_document(chat_id=GROUP_ID, document=str(ticket_file_id), caption=current_ticket_text, reply_markup=keyboard.options_ticket_cancellation_the_transaction_state() )
    await UserStates.wait.set()

async def admin_operations(GROUP_ID, call, state):
    split_ticket_id = call.message.caption
    split_ticket_id = split_ticket_id.split("\n")[0]
    await state.update_data(current_ticket=split_ticket_id)
    if call.data == "close_ticket_cancellation_the_transaction_state":
        await FeedbackModule.update_status(feedback_id=split_ticket_id, status="StatusType.CLOSED")
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=GROUP_ID, text="Тикет №" + str(split_ticket_id) + " закрыт")
    elif call.data == "status_ticket_cancellation_the_transaction_state":
        current_ticket_text = call.message.caption
        await state.update_data(current_ticket_text=current_ticket_text)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=GROUP_ID, text="Введите статус по данной заявке:")
        await UserStates.admin_group_status_cancellation_the_transaction.set()
    elif call.data == "answer_ticket_cancellation_the_transaction_state":
        current_ticket_text = call.message.caption
        await state.update_data(current_ticket_text=current_ticket_text)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=GROUP_ID, text="Введите свой ответ для клиента по данной заявке:")
        await UserStates.admin_group_answer_cancellation_the_transaction.set()