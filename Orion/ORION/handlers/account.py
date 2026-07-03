from aiogram.types import CallbackQuery
from datetime import datetime, timezone

from ORION.config import INVEST_TOKEN
from ORION.keyboards.portfolio import back_keyboard

from t_tech.invest.schemas import InstrumentIdType
from t_tech.invest import AsyncClient
from t_tech.invest.utils import quotation_to_decimal



async def account_view(callback: CallbackQuery):

    async with AsyncClient(
        INVEST_TOKEN,
        options=[
            (
                "grpc.ssl_target_name_override",
                "invest-public-api.tbank.ru"
            )
        ]
    ) as client:
        account_id = callback.data.replace("account_", "")

        portfolio = await client.operations.get_portfolio(
            account_id=account_id
        )
        positions = sorted(
            portfolio.positions,
            key=lambda x:
                (
                    quotation_to_decimal(x.current_price) *
                    quotation_to_decimal(x.quantity)
                    +
                    (
                        quotation_to_decimal(x.current_nkd) *
                        quotation_to_decimal(x.quantity)
                        if x.instrument_type == "bond"
                        else 0
                    )
                ),
            reverse=True
        )

        marginality = quotation_to_decimal(
            portfolio.total_amount_currencies
        ) * -1

        total = quotation_to_decimal(
            portfolio.total_amount_portfolio
        )

        marginality_value = ""
        total_double = ""
        if marginality > 0:
            marginality_value = f"🚩 Непокртые средства: <b>{marginality:,.2f} ₽</b>\n\n"
        if marginality > 0:
            total_double = f"💰 Всего: <b>{total:,.2f} ₽</b>\n"
        else:
            total_double =f"💰 Всего: <b>{total:,.2f} ₽</b>\n\n"

        text = (
            "📊 <b>Портфель</b>\n"
            f"{total_double}"
            f"{marginality_value}"
        )

        for position in positions:
            if position.ticker == "RUB000UTSTOM":
                continue

            quantity = quotation_to_decimal(
                position.quantity
            )

            current_price = quotation_to_decimal(
                position.current_price
            )

            nkd = quotation_to_decimal(
                position.current_nkd
            )

            if position.instrument_type == "bond":
                amount = (current_price * quantity) + (nkd * quantity)
            else:
                amount = current_price * quantity
            if amount <= 0:
                continue

            instrument = await client.instruments.get_instrument_by(
                id=position.instrument_uid,
                id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_UID
            )

            name = instrument.instrument.name

            next_payment = None
            payment_type = None

            now = datetime.now(timezone.utc)
            #купоны
            if position.instrument_type == "bond":

                coupons = await client.instruments.get_bond_coupons(
                    instrument_id=position.instrument_uid
                )

                future_coupons = []

                for coupon in coupons.events:
                    if now.date() <= coupon.coupon_date.date():
                        future_coupons.append(coupon)

                future_coupons.sort(
                    key=lambda x: x.coupon_date
                )

                if future_coupons:
                    next_payment = future_coupons[0]
                    payment_type = "coupon"

            #дивы
            elif position.instrument_type == "share":

                dividends = await client.instruments.get_dividends(
                    instrument_id=position.instrument_uid
                )

                future_dividends = []

                for dividend in dividends.dividends:
                    if now.date() <= dividend.payment_date.date():
                        future_dividends.append(dividend)

                future_dividends.sort(
                    key=lambda x: x.payment_date
                )

                if future_dividends:
                    next_payment = future_dividends[0]
                    payment_type = "dividend"

            extra = ""

            if position.instrument_type == "bond":
                extra += (
                    f"НКД: <b>{(nkd * quantity):,.2f} ₽</b>\n"
                )

            if next_payment:

                if payment_type == "coupon":

                    income = (
                            quotation_to_decimal(
                                next_payment.pay_one_bond
                            ) * quantity
                    )

                    extra += (
                        f"Купон: <b>{income:,.2f} ₽</b> "
                        f"(выплата {next_payment.coupon_date.strftime('%d.%m.%Y')})\n"
                    )


                elif payment_type == "dividend":

                    income = (
                            quotation_to_decimal(
                                next_payment.dividend_net
                            ) * quantity
                    )

                    extra += (
                        f"Дивиденд: <b>{income:,.2f} ₽</b> "
                        f"(выплата {next_payment.payment_date.strftime('%d.%m.%Y')})\n"
                    )


            text += (
                f"📌 <b>{name} ({position.ticker})</b>\n"
                f"Количество: <u>{int(quantity)}</u>\n"
                f"{extra}"
                f"Цена: <b>{current_price:,.2f} ₽</b>\n"
                f"Стоимость: <b>{amount:,.2f} ₽</b>\n\n"
            )

        await callback.message.edit_text(
            text,
            reply_markup=back_keyboard()
        )