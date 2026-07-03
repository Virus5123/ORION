from aiogram.types import CallbackQuery

from ORION.handlers.sectors import sectors
from ORION.handlers.portfolio import portfolio


async def back_accounts(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await portfolio(callback.message)

async def back_sectors(callback: CallbackQuery):
    await callback.message.delete()
    await sectors(callback.message)
    await callback.answer()