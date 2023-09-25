from dispatcher import bot
from states import UserStates
from repository import Ticket
from db import Database
from keyboards import add_comp, cancellation_the_transaction_type, ticket_list

config_file = 'config.ini'
db = Database(config_file)
ticket = Ticket(db)

async def main_menu(call, state):
    temp_data = await state.get_data()
    language = temp_data.get('language')
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if call.data == "card_reissue":
        await bot.send_message(chat_id=call.message.chat.id, text=language['27'])
        await UserStates.card_reissue.set()
    elif call.data == "ATM":
        await bot.send_message(chat_id=call.message.chat.id, text=language['2'], reply_markup=add_comp(language['5'], language['11'], language['14']))
    elif call.data == "cancellation_the_transaction":
        await bot.send_message(chat_id=call.message.chat.id, text=language['37'], reply_markup=cancellation_the_transaction_type())
    elif call.data == "tickets":
        user_id = call.message.chat.id
        result = ticket.select_ticket_card_reissue(user_id)
        ticket_num_counter = 0
        for ticket_num in result:
            if str(ticket_num[3]) == 'closed':
                ticket_num_counter = ticket_num_counter + 1

        atm_ticket_num_counter = 0
        result_atm_ticket = ticket.select_atm_ticket(user_id)
        for atm_ticket_num in result_atm_ticket:
            if str(atm_ticket_num[5]) == 'closed':
                atm_ticket_num_counter = atm_ticket_num_counter + 1
        
        if len(result) + len(result_atm_ticket) == ticket_num_counter + atm_ticket_num_counter:
            await bot.send_message(chat_id=call.message.chat.id, text=language['31'], reply_markup=ticket_list( language['24'], result, result_atm_ticket ))
        else:
            await bot.send_message(chat_id=call.message.chat.id, text=language['32'], reply_markup=ticket_list( language['24'], result, result_atm_ticket ))