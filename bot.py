import asyncio
import logging
from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.config_reader import load_config
from app.handlers.handler_common import register_handlers_common
from app.handlers.handler_show_words import register_handlers_words
from app.handlers.handler_training_words import register_handlers_training
from app.handlers.handler_quick_command import register_handlers_quick
from db.db_model import init_db
logger = logging.getLogger(__name__)


async def send_notification():
    logging.info('Notification')


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/words", description="Слова"),
        BotCommand(command="/training", description="Тренировка"),
        BotCommand(command="/stop", description="Выход в главное меню")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    # Инициализая базы данных
    init_db()
    # Парсинг файла конфигурации
    config = load_config("config/bot.ini")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())
    register_handlers_words(dp)
    register_handlers_common(dp)
    register_handlers_training(dp)
    register_handlers_quick(dp)

    await set_commands(bot)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())