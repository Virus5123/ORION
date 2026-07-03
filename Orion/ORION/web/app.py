# import os
# import certifi
# os.environ["SSL_CERT_FILE"] = certifi.where()
#
# from fastapi import FastAPI
# from fastapi.responses import FileResponse
#
# from t_tech.invest import AsyncClient
# from t_tech.invest.utils import quotation_to_decimal
# from pathlib import Path
# from ORION.web.services.portfolio import (
#     get_accounts,
#     get_portfolio,
#     get_total_portfolio
# )
# from ORION.config import INVEST_TOKEN
# BASE_DIR = Path(__file__).resolve().parent
# app = FastAPI()
#
#
# @app.get("/")
# async def home():
#     return FileResponse(
#         "bot_invest/web/index.html"
#     )
#
#
#
# @app.get("/accounts")
# async def accounts():
#
#     return await get_accounts()
#
#
#
# @app.get("/account/{account_id}")
# async def account(account_id: str):
#
#     total = await get_portfolio(
#         account_id
#     )
#
#     return {
#         "total": total
#     }
#
# @app.get("/portfolio")
# async def portfolio():
#
#     return await get_total_portfolio()