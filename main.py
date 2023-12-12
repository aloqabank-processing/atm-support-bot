from aiogram import executor
from dispatcher import dp
import controllers.atm_repair, controllers.cancel, controllers.card_reissue, controllers.feedback, controllers.menu_controller as cmd
# import bot as cmd

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
