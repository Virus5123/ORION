from decimal import Decimal

from t_tech.invest.schemas import InstrumentIdType
from t_tech.invest.utils import quotation_to_decimal
from ORION.services.cache import instrument_cache
from ORION.services.cache import asset_cache

async def load_sector_data(client):

    sector_data = {}

    accounts = await client.users.get_accounts()

    for account in accounts.accounts:

        try:
            portfolio = await client.operations.get_portfolio(
                account_id=account.id
            )

        except Exception:
            continue

        if not portfolio.positions:
            continue

        for position in portfolio.positions:

            if position.instrument_type == "CURRENCY":
                continue

            if position.ticker == "RUB000UTSTOM":
                continue

            quantity = quotation_to_decimal(position.quantity)
            price = quotation_to_decimal(position.current_price)
            nkd = quotation_to_decimal(position.current_nkd)

            if position.instrument_type == "bond":
                amount = price * quantity + nkd * quantity
            else:
                amount = price * quantity

            if amount <= 0:
                continue

            sector = "other"

            try:

                if position.instrument_uid in instrument_cache:
                    instrument = instrument_cache[position.instrument_uid]

                else:
                    instrument = await client.instruments.get_instrument_by(
                        id=position.instrument_uid,
                        id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_UID
                    )

                    instrument_cache[position.instrument_uid] = instrument

                asset_id = instrument.instrument.asset_uid

                if asset_id in asset_cache:
                    asset = asset_cache[asset_id]

                else:
                    asset = await client.instruments.get_asset_by(
                        id=asset_id
                    )

                    asset_cache[asset_id] = asset

                if asset.asset.brand:
                    if asset.asset.brand.sector:
                        sector = asset.asset.brand.sector

            except Exception:
                pass

            if sector not in sector_data:
                sector_data[sector] = {
                    "amount": Decimal("0"),
                    "positions": []
                }

            sector_data[sector]["amount"] += amount
            sector_data[sector]["positions"].append(
                {
                    "ticker": position.ticker,
                    "quantity": quantity,
                    "price": price,
                    "amount": amount,
                    "instrument_type": position.instrument_type,
                }
            )
    return sector_data
