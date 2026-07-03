# from decimal import Decimal
#
# from t_tech.invest import AsyncClient
# from t_tech.invest.utils import quotation_to_decimal
# from t_tech.invest.schemas import InstrumentIdType
#
# from ORION.config import INVEST_TOKEN
#
# async def get_accounts():
#
#     async with AsyncClient(
#         INVEST_TOKEN,
#         options=[
#             (
#                 "grpc.ssl_target_name_override",
#                 "invest-public-api.tbank.ru"
#             )
#         ]
#     ) as client:
#
#
#         accounts = await client.users.get_accounts()
#
#         result = []
#
#
#         for account in accounts.accounts:
#
#
#             pf = await client.operations.get_portfolio(
#                 account_id=account.id
#             )
#
#
#             total = quotation_to_decimal(
#                 pf.total_amount_portfolio
#             )
#
#
#             if total > 0.01:
#
#                 result.append({
#
#                     "id": account.id,
#
#                     "name": account.name,
#
#                     "total": float(total)
#
#                 })
#
#
#         return result
#
#
#
# async def get_portfolio(account_id):
#     async with AsyncClient(
#         INVEST_TOKEN,
#         options=[
#             (
#                 "grpc.ssl_target_name_override",
#                 "invest-public-api.tbank.ru"
#             )
#         ]
#     ) as client:
#         result = []
#         pf = await client.operations.get_portfolio(
#             account_id=account_id
#         )
#
#         for pos in pf.positions:
#             if pos.instrument_type == "CURRENCY":
#                 continue
#
#             quantity = quotation_to_decimal(
#                 pos.quantity
#             )
#             price = quotation_to_decimal(
#                 pos.current_price
#             )
#             amount = quantity * price
#
#             if amount <= 0:
#                 continue
#
#             instrument = await client.instruments.get_instrument_by(
#                 id=pos.instrument_uid,
#                 id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_UID
#             )
#
#             result.append({
#                 "name":
#                     instrument.instrument.name,
#                 "ticker":
#                     instrument.instrument.ticker,
#                 "quantity":
#                     float(quantity),
#                 "amount":
#                     float(amount)
#             })
#
#         total = sum(
#             x["amount"]
#             for x in result
#         )
#
#         return {
#             "total": total,
#             "items": result
#         }
#
# async def get_total_portfolio():
#
#     async with AsyncClient(
#         INVEST_TOKEN,
#         options=[
#             (
#                 "grpc.ssl_target_name_override",
#                 "invest-public-api.tbank.ru"
#             )
#         ]
#     ) as client:
#
#
#         accounts = await client.users.get_accounts()
#
#
#         positions = {}
#
#
#         for account in accounts.accounts:
#
#
#             pf = await client.operations.get_portfolio(
#                 account_id=account.id
#             )
#
#
#             for pos in pf.positions:
#
#
#                 if pos.instrument_type == "CURRENCY":
#                     continue
#
#
#                 quantity = quotation_to_decimal(
#                     pos.quantity
#                 )
#
#
#                 price = quotation_to_decimal(
#                     pos.current_price
#                 )
#
#
#                 amount = quantity * price
#
#
#                 if amount <= 0:
#                     continue
#
#
#                 uid = pos.instrument_uid
#
#
#                 if uid not in positions:
#
#
#                     instrument = await client.instruments.get_instrument_by(
#                         id=uid,
#                         id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_UID
#                     )
#
#
#                     positions[uid] = {
#
#                         "name":
#                             instrument.instrument.name,
#
#                         "ticker":
#                             instrument.instrument.ticker,
#
#                         "quantity":
#                             Decimal("0"),
#
#                         "amount":
#                             Decimal("0")
#                     }
#
#
#
#                 positions[uid]["quantity"] += quantity
#                 positions[uid]["amount"] += amount
#
#
#
#         total = sum(
#             x["amount"]
#             for x in positions.values()
#         )
#
#
#
#         result = []
#
#
#         for x in sorted(
#             positions.values(),
#             key=lambda x:x["amount"],
#             reverse=True
#         ):
#
#
#             result.append({
#
#                 "name": x["name"],
#
#                 "ticker": x["ticker"],
#
#                 "quantity":
#                     float(x["quantity"]),
#
#                 "amount":
#                     float(x["amount"])
#
#             })
#
#
#         return {
#
#             "total":
#                 float(total),
#
#             "items":
#                 result
#
#         }