import logging
from aiogram import Bot, Dispatcher, F
from asyncio import run
from aiogram.types import BotCommand
from aiogram.filters import Command

from config import API_TOKEN

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

dp = Dispatcher()

async def main():
    bot = Bot(token=API_TOKEN)
    
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
