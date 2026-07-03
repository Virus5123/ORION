from aiogram.types import CallbackQuery
from decimal import Decimal
from datetime import datetime, timezone

from ORION.keyboards.portfolio import back_keyboard
from ORION.config import INVEST_TOKEN

from t_tech.invest import AsyncClient
from t_tech.invest.utils import quotation_to_decimal
from t_tech.invest.schemas import InstrumentIdType


async def total_portfolio_view(callback: CallbackQuery):

    await callback.answer()

    async with AsyncClient(
        INVEST_TOKEN,
        options=[
            (
                "grpc.ssl_target_name_override",
                "invest-public-api.tbank.ru"
            )
        ]
    ) as client:

        accounts = await client.users.get_accounts()

        positions = {}

        for account in accounts.accounts:

            portfolio = await client.operations.get_portfolio(
                account_id=account.id
            )

            for pos in portfolio.positions:

                # убираем рубли и валюту
                if pos.instrument_type == "CURRENCY":
                    continue

                nkd = quotation_to_decimal(pos.current_nkd)
                quantity = quotation_to_decimal(pos.quantity)
                price = quotation_to_decimal(pos.current_price)

                if pos.instrument_type == "bond":
                    amount = (price * quantity) + (nkd * quantity)
                else:
                    amount = price * quantity
                if amount <= 0:
                    continue

                uid = pos.instrument_uid
                if uid not in positions:

                    instrument = await client.instruments.get_instrument_by(
                        id=uid,
                        id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_UID
                    )
                    positions[uid] = {
                        "name": instrument.instrument.name,
                        "ticker": instrument.instrument.ticker,
                        "quantity": Decimal("0"),
                        "amount": Decimal("0"),
                        "nkd": Decimal("0"),
                        "type": pos.instrument_type,
                        "uid": uid
                    }


                positions[uid]["quantity"] += quantity
                positions[uid]["amount"] += amount
                positions[uid]["nkd"] += nkd * quantity

        total = sum(
            item["amount"]
            for item in positions.values()
        )

        if total == 0:
            await callback.message.answer(
                "Портфель пуст"
            )
            return

        text = "<b>🌍 Общий портфель</b>\n\n"

        for item in sorted(
            positions.values(),
            key=lambda x: x["amount"],
            reverse=True
        ):
            share = (
                item["amount"]
                / total
                * 100
            )

            quantity = item["quantity"].to_integral_value()

            extra = ""

            now = datetime.now(timezone.utc)

            if item["type"] == "bond":

                extra += (
                    f"НКД: <b>{item['nkd']:.2f} ₽</b>\n"
                )

                coupons = await client.instruments.get_bond_coupons(
                    instrument_id=item["uid"]
                )

                future_coupons = []

                for coupon in coupons.events:
                    if now.date() <= coupon.coupon_date.date():
                        future_coupons.append(coupon)

                future_coupons.sort(
                    key=lambda x: x.coupon_date
                )

                if future_coupons:
                    next_coupon = future_coupons[0]

                    coupon_amount = (
                            quotation_to_decimal(
                                next_coupon.pay_one_bond
                            )
                            *
                            item["quantity"]
                    )

                    extra += (
                        f"Купон: <b>{coupon_amount:.2f} ₽</b> "
                        f"(выплата {next_coupon.coupon_date.strftime('%d.%m.%Y')})\n"
                    )


            elif item["type"] == "share":

                dividends = await client.instruments.get_dividends(
                    instrument_id=item["uid"]
                )

                future_dividends = []

                for dividend in dividends.dividends:
                    if now.date() <= dividend.payment_date.date():
                        future_dividends.append(dividend)

                future_dividends.sort(
                    key=lambda x: x.payment_date
                )

                if future_dividends:
                    next_dividend = future_dividends[0]

                    dividend_amount = (
                            quotation_to_decimal(
                                next_dividend.dividend_net
                            )
                            *
                            item["quantity"]
                    )

                    extra += (
                        f"Дивиденд: <b>{dividend_amount:.2f} ₽</b> "
                        f"(выплата {next_dividend.payment_date.strftime('%d.%m.%Y')})\n"
                    )

            text += (
                f"📌 <b>{item['name']} ({item['ticker']})</b>\n"
                f"Количество: <u>{quantity}</u>\n"
                f"Стоимость: <b>{item['amount']:.2f} ₽</b>\n"
                f"{extra}"
                f"Доля: <i>{share:.2f}%</i>\n\n"
            )



        await callback.message.edit_text(
            text,
            reply_markup=back_keyboard()
        )