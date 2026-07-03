from aiogram.types import Message
from ORION.keyboards.portfolio import accounts_keyboard
from ORION.services.portfolio_service import load_portfolio_data


async def portfolio(message: Message):

    data = await load_portfolio_data(message.from_user.id)

    income_text = ""

    for month in set(data["income"]["coupons"]) | set(data["income"]["dividends"]):

        coupons = data["income"]["coupons"].get(month, 0)
        dividends = data["income"]["dividends"].get(month, 0)

        total = coupons + dividends

        income_text += (
            f"📅 {month}: <b>{total:.2f} ₽</b>\n"
            f" ├ Купоны: <b>{coupons:.2f}</b>\n"
            f" └ Дивиденды: <b>{dividends:.2f}</b>\n\n"
        )

    extra = ""
    if data["total_marginality"] > 0:
        extra = f"🚩 Непокрытые средства: <b>{data['total_marginality']:,.2f}</b>\n\n"

    await message.answer(
        f"💼 <b>Портфель</b>\n\n"
        f"💰 Всего: <b>{data['total_money']:,.2f}</b>\n"
        f"{extra}"
        f"{income_text}"
        f"Выберите счёт:",
        reply_markup=accounts_keyboard(data["accounts"])
    )