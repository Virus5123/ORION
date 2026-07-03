import asyncio
import threading
import subprocess
import time
import sys
from pathlib import Path
import sqlite3
from pathlib import Path

# import uvicorn
# from pyngrok import ngrok
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram import Router

from ORION.config import TG_TOKEN
from ORION.db.init_db import init_db
from ORION.db.database import get_connection

bot = Bot(
    token=TG_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()
router = Router()
dp.include_router(router)
DB_PATH = Path("bot_invest.db")

from ORION.handlers.start import start
dp.message.register(start, Command("start"))

from ORION.handlers.portfolio import portfolio
from ORION.handlers.account import account_view
from ORION.handlers.total_portfolio import total_portfolio_view
from ORION.handlers.back import back_accounts, back_sectors

dp.message.register(portfolio, F.text == "💼 Портфель")
dp.callback_query.register(
    account_view,
    lambda c: c.data.startswith("account_")
)
dp.callback_query.register(
    total_portfolio_view,
    lambda c: c.data == "total_portfolio"
)
router.callback_query.register(
    back_accounts,
    lambda c: c.data == "back_accounts"
)

from ORION.handlers.sectors import sectors
from ORION.handlers.sector_details import sector_detail
from ORION.keyboards.sector_keyboard import sector_back_keyboard
dp.message.register(sectors, F.text == "📊 Сектора")
dp.callback_query.register(
    sector_detail,
    lambda c: c.data.startswith("sector:")
)
router.callback_query.register(
    back_sectors,
    lambda c: c.data == "back_sectors"
)
# def run_web():
#     uvicorn.run(
#         "bot_invest.web.app:app",
#         host="127.0.0.1",
#         port=8000
#     )

# def run_ngrok():
#     ngrok.kill()
#     tunnel = ngrok.connect(8000)
#     print(
#         "Ngrok URL:",
#         tunnel.public_url
#     )

async def main():
    init_db()
    # threading.Thread(
    #     target=run_web,
    #     daemon=True
    # ).start()
    #
    #
    # threading.Thread(
    #     target=run_ngrok,
    #     daemon=True
    # ).start()

    print("База инициализирована")
    print("Бот запущен")
    # print("Web запущен")
    # print("Ngrok запускается")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
