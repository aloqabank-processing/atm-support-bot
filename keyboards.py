from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def share_keyboard():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton(
        text="📱 Отправить", request_contact=True)
    keyboard.add(button)
    return keyboard

def send_location(text_for_location):
    keyboard = ReplyKeyboardMarkup()
    button = KeyboardButton(text_for_location, request_location=True)
    keyboard.add(button)
    return keyboard

def choose_language():
    buttons = [
        InlineKeyboardButton(text="Ru", callback_data="Ru"),
        InlineKeyboardButton(text="Uz", callback_data="Uz"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def add_comp(text_for_add, text_for_card, text_for_cash_out):
    buttons = [
        InlineKeyboardButton(text=text_for_card, callback_data="card"),
        InlineKeyboardButton(text=text_for_cash_out, callback_data="cashout"),
        InlineKeyboardButton(text=text_for_add, callback_data="add"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

def Continue(cont):
    buttons = [
        InlineKeyboardButton(text=cont, callback_data="cont"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def no_photo(text_for_add, text_for_enter):
    buttons = [
        InlineKeyboardButton(text=text_for_add, callback_data="noPhoto"),
        InlineKeyboardButton(text=text_for_enter, callback_data="enter"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

def choose_problem(text_for_card_reissue, text_for_ATM, text_for_tickets, text_for_cancellation_the_transaction, text_for_atm_repair ):
    buttons = [
        InlineKeyboardButton(text=text_for_cancellation_the_transaction, callback_data="cancellation_the_transaction"),
        InlineKeyboardButton(text=text_for_card_reissue, callback_data="card_reissue"),
        InlineKeyboardButton(text=text_for_atm_repair, callback_data="atm_repair"),
        InlineKeyboardButton(text=text_for_tickets, callback_data="tickets"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

def choose_problem_user(text_for_card_reissue, text_for_ATM, text_for_tickets):
    buttons = [
        InlineKeyboardButton(text=text_for_ATM, callback_data="ATM"),
        InlineKeyboardButton(text=text_for_tickets, callback_data="tickets"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

def method_to_choose_ATM(text_for_location, text_for_QR, text_for_back_from_choose_ATM):
    buttons = [
        InlineKeyboardButton(text=text_for_location, callback_data="location"),
        InlineKeyboardButton(text=text_for_QR, callback_data="QR"),
        InlineKeyboardButton(text=text_for_back_from_choose_ATM, callback_data="back_from_choose_ATM"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

def back_to_choose_ATM(text_for_back_from_choose_ATM):
    buttons = [
        InlineKeyboardButton(text=text_for_back_from_choose_ATM, callback_data="back_from_choose_ATM"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

def options_ticket_card_reissue():
    buttons = [
        InlineKeyboardButton(text="ОСТАВИТЬ ОТВЕТ", callback_data="answer_ticket_card_reissue"),
        InlineKeyboardButton(text="ИЗМЕНИТЬ СТАТУС", callback_data="status_ticket_card_reissue"),
        InlineKeyboardButton(text="ЗАКРЫТЬ ТИКЕТ", callback_data="close_ticket_card_reissue"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

def options_ticket_atm_repair():
    buttons = [
        InlineKeyboardButton(text="ОСТАВИТЬ ОТВЕТ", callback_data="answer_ticket_atm_repair"),
        InlineKeyboardButton(text="ИЗМЕНИТЬ СТАТУС", callback_data="status_ticket_atm_repair"),
        InlineKeyboardButton(text="ЗАКРЫТЬ ТИКЕТ", callback_data="close_ticket_atm_repair"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

def options_ticket_cancellation_the_transaction_state():
    buttons = [
        InlineKeyboardButton(text="ОСТАВИТЬ ОТВЕТ", callback_data="answer_ticket_cancellation_the_transaction_state"),
        InlineKeyboardButton(text="ИЗМЕНИТЬ СТАТУС", callback_data="status_ticket_cancellation_the_transaction_state"),
        InlineKeyboardButton(text="ЗАКРЫТЬ ТИКЕТ", callback_data="close_ticket_cancellation_the_transaction_state"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

def options_atm_ticket():
    buttons = [
        InlineKeyboardButton(text="ОСТАВИТЬ ОТВЕТ", callback_data="answer_atm_ticket"),
        InlineKeyboardButton(text="ИЗМЕНИТЬ СТАТУС", callback_data="status_atm_ticket"),
        InlineKeyboardButton(text="ЗАКРЫТЬ ТИКЕТ", callback_data="close_atm_ticket"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

def cancellation_the_transaction_type():
    buttons = [
        InlineKeyboardButton(text="HUMO", callback_data="HUMO"),
        InlineKeyboardButton(text="UZCARD", callback_data="UZCARD"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

def ticket_list( text_for_back_from_choose_ATM, tickets_from_current_user, atm_tickets_from_current_user ):

    keyboard = InlineKeyboardMarkup(row_width=1)


    if len(tickets_from_current_user) + len(atm_tickets_from_current_user) == 0:
        button = InlineKeyboardButton(text=text_for_back_from_choose_ATM, callback_data="back_from_choose_ATM")
        keyboard.add(button)
        return keyboard
    
    ticket_num_counter = 0
    for ticket_num in tickets_from_current_user:
        if str(ticket_num[3]) == 'closed':
            ticket_num_counter = ticket_num_counter + 1

    atm_ticket_num_counter = 0

    for ticket_num in atm_tickets_from_current_user:
        if str(ticket_num[5]) == 'closed':
            atm_ticket_num_counter = atm_ticket_num_counter + 1
    
    else: 
        for ticket_num in tickets_from_current_user:
            if str(ticket_num[3]) != 'closed':
                button = InlineKeyboardButton(text='Заявка №' + str(ticket_num[0]), callback_data=int(ticket_num[0]))
                keyboard.add(button)

        for ticket_num in atm_tickets_from_current_user:
            
            if str(ticket_num[5]) != 'closed':
                print(ticket_num)
                button = InlineKeyboardButton(text='ATM №' + str(ticket_num[0]), callback_data=int(ticket_num[0]))
                keyboard.add(button)

    button = InlineKeyboardButton(text=text_for_back_from_choose_ATM, callback_data="back_from_choose_ATM")
    keyboard.add(button)

    return keyboard

def filial_list( text_for_back_from_choose_ATM ):
    buttons = [
        InlineKeyboardButton(text="Amaliyot", callback_data="Amaliyot"),
        InlineKeyboardButton(text="Qoraqalpogiston", callback_data="Qoraqalpogiston"),
        InlineKeyboardButton(text="Xorazm", callback_data="Xorazm"),
        InlineKeyboardButton(text="Namangan", callback_data="Namangan"),
        InlineKeyboardButton(text="Andijon", callback_data="Andijon"),
        InlineKeyboardButton(text="Buxoro", callback_data="Buxoro"),
        InlineKeyboardButton(text="Surxondaryo", callback_data="Surxondaryo"),
        InlineKeyboardButton(text="Samarqand", callback_data="Samarqand"),
        InlineKeyboardButton(text="Qashqadaryo", callback_data="Qashqadaryo"),
        InlineKeyboardButton(text="Navoiy", callback_data="Navoiy"),
        InlineKeyboardButton(text="Fargona", callback_data="Fargona"),
        InlineKeyboardButton(text="Jizzax", callback_data="Jizzax"),
        InlineKeyboardButton(text="Qoqon", callback_data="Qoqon"),        
        InlineKeyboardButton(text=text_for_back_from_choose_ATM, callback_data="back_from_choose_ATM"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

def model_list( model, text_for_back_from_choose_ATM ):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for temp_model in model:
        button = InlineKeyboardButton(text=str(temp_model), callback_data=str(temp_model))
        keyboard.add(button)
    button = InlineKeyboardButton(text=text_for_back_from_choose_ATM, callback_data="back_from_choose_ATM")
    keyboard.add(button)
    return keyboard

def terminal_id_list( terminal_id, text_for_back_from_choose_ATM ):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for temp_terminal_id in terminal_id:
        button = InlineKeyboardButton(text=str(temp_terminal_id[0]), callback_data=str(temp_terminal_id[0]))
        keyboard.add(button)
    button = InlineKeyboardButton(text=text_for_back_from_choose_ATM, callback_data="back_from_choose_ATM")
    keyboard.add(button)
    return keyboard