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

def choose_problem(text_for_card_reissue, text_for_ATM, text_for_tickets):
    buttons = [
        InlineKeyboardButton(text=text_for_card_reissue, callback_data="card_reissue"),
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
