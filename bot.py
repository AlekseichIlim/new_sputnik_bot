from config import DEBUG, bot
import logging
from aiogram import Dispatcher
import asyncio
from sp_bot.handlers.admin_handlers import admin_router_sp


async def main():
    # await create_all_tables(engine)
    # await save_names_brigades(pl_list)

    dp = Dispatcher()
    #
    # # dp.include_router(admin_router)
    # # dp.include_router(user_router)
    dp.include_router(admin_router_sp)


    await dp.start_polling(bot)
    # await bot.delete_webhook()
    # await bot.delete_webhook(drop_pending_updates=True)

if __name__ == '__main__':
    if DEBUG:
        logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
