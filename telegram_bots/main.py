import asyncio
import logging
import sys

from aiogram import Bot,Dispatcher
from aiogram.enums import ParseMode

from cmd_handler import cmd_router
from message_handler import msg_router
from config import TOKEN


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(cmd_router,msg_router)
    await dp.start_polling(bot)
    
   
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')