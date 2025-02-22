import logging
from aiogram import Bot, Dispatcher
from asyncio import run
from aiogram.types import BotCommand

import user_side
import admin_panel

from config import API_TOKEN

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

dp = Dispatcher()
async def startup_answer(bot : Bot):
    await bot.send_message(746617254, "bot ishga tushdi🙌")
async  def shutdown_answer(bot : Bot):
    await bot.send_message(746617254, "bot ishdan toxtadi")


async def main():
    bot = Bot(token=API_TOKEN)
    dp.startup.register(startup_answer)
    dp.include_router(user_side.router)
    dp.include_router(admin_panel.router)
    dp.shutdown.register(shutdown_answer)

    
    logger.info("Bot is starting...")
    
    try:
        await bot.set_my_commands([
            BotCommand(command="/start", description="Botni ishga tushirish"),
            BotCommand(command="/lang", description="Tilni o'zgartirish")
        ])
        logger.info("Bot commands set successfully.")
        
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        await bot.session.close()
        logger.info("Bot session closed.")

if __name__ == '__main__':
    run(main())
