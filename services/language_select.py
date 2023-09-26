from dispatcher import bot
from states import UserStates
from repository import User
from db import Database
import keyboards as keyboard
from lang import get_language

config_file = 'config.ini'
db = Database(config_file)
user = User(db)

async def admin_exist(user_id, chat_id, message, state):
    if user.admin_exists(user_id):
        await bot.send_message(chat_id=chat_id, text="🇷🇺Сюда вам будут приходить жалобы и предложения по вашему региону \n🇺🇿Bu erda sizning mintaqangiz bo'yicha shikoyatlar va takliflar keladi")
    elif not user.exists(user_id):
        print('not')
        await UserStates.NotExist.set()
        await bot.send_message(chat_id=chat_id, text="🇷🇺Выберите язык \n🇺🇿Tilni tanlang", reply_markup=keyboard.choose_language())
    else:
        print('yes')
        await UserStates.Exist.set()
        await state.update_data(user_id=user_id)
        await bot.send_message(chat_id=message.chat.id, text="🇷🇺Выберите язык \n🇺🇿Tilni tanlang", reply_markup=keyboard.choose_language())

async def select_language(FILIAL, call, state):
    current_state = await state.get_state()

    await call.answer('Done')
    language = get_language(call.data)

    if language is not None:

        await state.update_data(language=language)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language['7'])

        if current_state == 'UserStates:Exist':
            if str(call.message.chat.id) == FILIAL:
                await bot.send_message(chat_id=call.message.chat.id, text=language['20'], reply_markup=keyboard.choose_problem(language['18'], language['17'], language['19'], language['34']))
            else:
                await bot.send_message(chat_id=call.message.chat.id, text=language['20'], reply_markup=keyboard.choose_problem_user(language['18'], language['17'], language['19']))     
        elif current_state == 'UserStates:NotExist':
            msg = await bot.send_message(chat_id=call.message.chat.id, text=language['1'], reply_markup=keyboard.share_keyboard())
            await state.update_data(lang_msg_id=msg.message_id)

async def registation(GROUP_ID, message, state):
    phone = message.contact.phone_number
    name = message.from_user.full_name
    user_id = message.from_user.id
    await state.update_data(user_id=user_id)
    user.add(name, phone, user_id)

    temp_data = await state.get_data()
    message_id = temp_data.get('lang_msg_id')

    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    await bot.delete_message(chat_id=user_id, message_id=message_id)

    language = temp_data.get('language')

    if str(message.chat.id) == GROUP_ID:
        await bot.send_message(chat_id=message.chat.id, text=language['20'], reply_markup=keyboard.choose_problem(language['18'], language['17'], language['19'], language['34']))
    else:
        await bot.send_message(chat_id=message.chat.id, text=language['20'], reply_markup=keyboard.choose_problem_user(language['18'], language['17'], language['19']))