from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ORION.services.cache import sector_cache

async def sector_detail(callback: CallbackQuery):

    sector = callback.data.split(":")[1]

    data = sector_cache.get(sector)

    if not data:
        await callback.answer(
            "Сектор пуст",
            show_alert=True
        )
        return

    print("ДАННЫЕ СЕКТОРА:", data)
    total = data["amount"]
    positions = data["positions"]

    text = (
        f"<b>📊 {sector}</b>\n\n"
        f"💰 Сумма сектора: <b>{total:.2f} ₽</b>\n\n"
    )

    for pos in positions:
        part = float(pos["amount"] / total * 100)

        text += (
            f"📌 <b>{pos['ticker']}</b>\n"
            f"Количество: {pos['quantity']:.2f}\n"
            f"Цена: <u>{pos['price']:.2f}</u> ₽\n"
            f"Сумма: <b>{pos['amount']:.2f} ₽</b>\n"
            f"Доля: <i>{part:.2f}%</    i>\n\n"
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="back_sectors"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        text,
        reply_markup=keyboard
    )

    await callback.answer()