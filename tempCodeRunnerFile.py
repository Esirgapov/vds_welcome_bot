import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
# from aiogram.types.chat_member import ChatMember
# from aiogram.utils.chat_action import ChatActionSender

from aiogram.types import (
    BotCommandScopeDefault,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllChatAdministrators
)
from config_data.config import Config, load_config
from handlers import user_handlers

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')
    config: Config = load_config()
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_router(user_handlers.router)
    await bot.delete_my_commands(scope=BotCommandScopeDefault())
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await bot.delete_my_commands(scope=BotCommandScopeAllGroupChats())
    await bot.delete_my_commands(scope=BotCommandScopeAllChatAdministrators())    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
