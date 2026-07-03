from decimal import Decimal

from aiogram.types import Message

from t_tech.invest import AsyncClient

from ORION.services.cache import sector_cache
from ORION.keyboards.sector_keyboard import sectors_keyboard
from ORION.config import INVEST_TOKEN
from ORION.utils.sector_info import ICONS, TRANSLATE
from ORION.utils.progress import progress_bar
from ORION.services.sector_service import load_sector_data
from ORION.keyboards.sector_keyboard import sectors_keyboard

async def sectors(message: Message):

    async with AsyncClient(
        INVEST_TOKEN,
        options=[
            (
                "grpc.ssl_target_name_override",
                "invest-public-api.tbank.ru"
            )
        ]
    ) as client:

        sector_data = await load_sector_data(client)


        sector_cache.clear()
        sector_cache.update(sector_data)

        if not sector_data:
            await message.answer(
                "📊 Сектора\n\nПортфель пуст"
            )
            return

        total = sum(
            data["amount"]
            for data in sector_data.values()
        )

        text = "<b>📊 Сектора портфеля</b>\n\n"

        for sector, data in sorted(
                sector_data.items(),
                key=lambda x: x[1]["amount"],
                reverse=True
        ):
            amount = data["amount"]

            percent = float(amount / total * 100)

            text += (
                f"{ICONS.get(sector, '📦')} "
                f"<b>{TRANSLATE.get(sector, sector)}</b> "
                f"<b>{percent:.2f}%</b>\n"
                f"{progress_bar(percent)}\n\n"
            )

        buttons = []

        for sector, data in sorted(
                sector_data.items(),
                key=lambda x: x[1]["amount"],
                reverse=True
        ):
            buttons.append(
                (
                    sector,
                    f"{ICONS.get(sector, '📦')} {TRANSLATE.get(sector, sector)}"
                )
            )

        await message.answer(
            text,
            reply_markup=sectors_keyboard(buttons)
        )
