import asyncio
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

from t_tech.invest import AsyncClient
from t_tech.invest.utils import quotation_to_decimal

from ORION.config import INVEST_TOKEN
from ORION.services.db_sync import (
    upsert_account,
    upsert_instrument,
    upsert_portfolio
)

months = {
    "January": "январь",
    "February": "февраль",
    "March": "март",
    "April": "апрель",
    "May": "май",
    "June": "июнь",
    "July": "июль",
    "August": "август",
    "September": "сентябрь",
    "October": "октябрь",
    "November": "ноябрь",
    "December": "декабрь"
}


async def load_portfolio_data(user_id: int):
    async with AsyncClient(
        INVEST_TOKEN,
        options=[
            ("grpc.ssl_target_name_override", "invest-public-api.tbank.ru")
        ]
    ) as client:

        accounts = await client.users.get_accounts()

        # 🔥 sync accounts
        for acc in accounts.accounts:
            upsert_account(user_id, acc.id)

        portfolios = await asyncio.gather(
            *[
                client.operations.get_portfolio(account_id=a.id)
                for a in accounts.accounts
            ]
        )

        income = {"coupons": {}, "dividends": {}}
        now = datetime.now(timezone.utc)
        month_later = now + relativedelta(months=1)

        total_money = 0
        total_marginality = 0
        dfa = 0
        active_accounts = []

        for account, p in zip(accounts.accounts, portfolios):

            total = quotation_to_decimal(p.total_amount_portfolio)
            marginality = quotation_to_decimal(p.total_amount_currencies)

            if total > 0.01:
                total_money += total
                total_marginality += marginality
                active_accounts.append(account)

            dfa_amount = quotation_to_decimal(p.total_amount_dfa)

            if dfa_amount > 0.01:
                dfa += dfa_amount
                if account not in active_accounts:
                    if account not in active_accounts:
                        active_accounts.append(account)

            for position in p.positions:

                if position.instrument_type not in ["bond", "share"]:
                    continue

                qty = quotation_to_decimal(position.quantity)

                # 🔥 DB sync instrument
                upsert_instrument(
                    uid=position.instrument_uid,
                    ticker=position.ticker,
                    name=position.ticker,
                    sector="unknown",
                    instrument_type=position.instrument_type
                )

                # 🔥 DB sync portfolio
                upsert_portfolio(
                    account_id=account.id,
                    instrument_uid=position.instrument_uid,
                    quantity=qty,
                    avg_price=quotation_to_decimal(position.average_position_price)
                )

                # coupons
                if position.instrument_type == "bond":
                    coupons = await client.instruments.get_bond_coupons(
                        instrument_id=position.instrument_uid
                    )

                    for c in coupons.events:
                        if now.date() <= c.coupon_date.date() <= month_later.date():
                            pay = quotation_to_decimal(c.pay_one_bond)
                            month = months[c.coupon_date.strftime("%B")]
                            income["coupons"][month] = income["coupons"].get(month, 0) + pay * qty

                # dividends
                if position.instrument_type == "share":
                    try:
                        divs = await client.instruments.get_dividends(
                            instrument_id=position.instrument_uid
                        )
                    except Exception:
                        continue

                    for d in divs.dividends:
                        if now.date() <= d.payment_date.date() <= month_later.date():
                            pay = quotation_to_decimal(d.dividend_net)
                            month = months[d.payment_date.strftime("%B")]
                            income["dividends"][month] = income["dividends"].get(month, 0) + pay * qty

        return {
            "total_money": total_money + dfa,
            "total_marginality": total_marginality * -1,
            "income": income,
            "accounts": active_accounts
        }