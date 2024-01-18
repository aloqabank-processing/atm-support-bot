from dispatcher import bot
from states import UserStates
import keyboards as keyboard
from lang import get_language
from api_query import AdministrationModule

async def admin_exist(user_id, chat_id, message, state):
    if not AdministrationModule.get_user(user_id):
        await UserStates.NotExist.set()
        await bot.send_message(chat_id=chat_id, text="🇷🇺Выберите язык \n🇺🇿Tilni tanlang", reply_markup=keyboard.choose_language())
    else:
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
                await bot.send_message(chat_id=call.message.chat.id, text=language['20'], reply_markup=keyboard.choose_problem(language['18'], language['17'], language['19'], language['34'], language['39']))
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
    await AdministrationModule.add_user(name, phone, user_id)

    temp_data = await state.get_data()
    message_id = temp_data.get('lang_msg_id')

    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    await bot.delete_message(chat_id=user_id, message_id=message_id)

    language = temp_data.get('language')

    if str(message.chat.id) == GROUP_ID:
        await bot.send_message(chat_id=message.chat.id, text=language['20'], reply_markup=keyboard.choose_problem(language['18'], language['17'], language['19'], language['34'], language['39']))
    else:
        await bot.send_message(chat_id=message.chat.id, text=language['20'], reply_markup=keyboard.choose_problem_user(language['18'], language['17'], language['19']))