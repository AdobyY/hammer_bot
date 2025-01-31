import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

from app.handlers import router


load_dotenv()

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    logger.info("Бот запущено і готовий до роботи")
    print("^^^^^^ Запуск бота ^^^^^^")

    await dp.start_polling(bot)

if __name__=='__main__':
    asyncio.run(main())