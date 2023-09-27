from dispatcher import bot
from states import UserStates
from repository import Ticket
from db import Database
import keyboards as keyboard
from datetime import datetime

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
        await bot.send_message(chat_id=call.message.chat.id, text=language['2'], reply_markup=keyboard.add_comp(language['5'], language['11'], language['14']))
    elif call.data == "cancellation_the_transaction":
        await bot.send_message(chat_id=call.message.chat.id, text=language['37'], reply_markup=keyboard.cancellation_the_transaction_type())
    elif call.data == "atm_repair":
        await bot.send_message(chat_id=call.message.chat.id, text=language['40'], reply_markup=keyboard.filial_list(language['24']))
    else:
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
            await bot.send_message(chat_id=call.message.chat.id, text=language['31'], reply_markup=keyboard.ticket_list( language['24'], result, result_atm_ticket ))
        else:
            await bot.send_message(chat_id=call.message.chat.id, text=language['32'], reply_markup=keyboard.ticket_list( language['24'], result, result_atm_ticket ))
    
async def ticket_menu(call, state):
    number = int(call.data)

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    temp_data = await state.get_data()
    language = temp_data.get('language')

    result = ticket.ticket_by_ticket_id(number)
    atm_result = ticket.atm_ticket_by_ticket_id(number)

    if len(result) != 0:
        result_of_selection = result[0]
        if str(result_of_selection[5]) == 'card_reissue' or str(result_of_selection[5]) == 'UZCARD':
            client_ticket_form = language['28'] + str(number) + "\n" + result_of_selection[2] + "\n" + language['29'] + result_of_selection[3] + "\n" + language['30'] + result_of_selection[4]

            msg = await bot.send_message(chat_id=call.message.chat.id, text=client_ticket_form, reply_markup=keyboard.back_to_choose_ATM(language['24']))
            await state.update_data(button=msg.message_id)
        else:
            client_ticket_form = language['28'] + str(number) + "\n" + language['29'] + result_of_selection[3] + "\n" + language['30'] + result_of_selection[4]

            await bot.send_document(chat_id=call.message.chat.id, document=str(result_of_selection[2]), caption=client_ticket_form, reply_markup=keyboard.back_to_choose_ATM(language['24']))

    if len(atm_result) != 0:
        result_of_selection = atm_result[0]

        client_ticket_form = language['28'] + str(number) + "\n" + result_of_selection[2] + "\n" + language['29'] + result_of_selection[5] + "\n" + language['30'] + result_of_selection[6]

        msg = await bot.send_message(chat_id=call.message.chat.id, text=client_ticket_form, reply_markup=keyboard.back_to_choose_ATM(language['24']))
        await state.update_data(button=msg.message_id)

async def next(FILIAL, call, state):
    temp_data = await state.get_data()
    language = temp_data.get('language')

    current_hour = datetime.now().hour
    current_day = datetime.now().weekday()

    if current_hour < 9 or current_hour >= 18 or current_day > 5:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = language['6'] )
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = language['4'] )

    if str(call.message.chat.id) == FILIAL:
        msg = await bot.send_message(chat_id=call.message.chat.id, text=language['20'], reply_markup=keyboard.choose_problem(language['18'], language['17'], language['19'], language['34'], language['39']))
        await state.update_data(button=msg.message_id)
    else:
        msg = await bot.send_message(chat_id=call.message.chat.id, text=language['20'], reply_markup=keyboard.choose_problem_user(language['18'], language['17'], language['19']))
        await state.update_data(button=msg.message_id)