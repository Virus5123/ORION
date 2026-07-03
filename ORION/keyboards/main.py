from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo
)


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💼 Портфель"),
            KeyboardButton(text="📊 Сектора")
        ],
        # [
        #     KeyboardButton(
        #         text="🚀 Открыть приложение",
        #         web_app=WebAppInfo(
        #             url="https://gorgeous-boil-haven.ngrok-free.dev"
        #         )
        #     )
        # ]
    ],
    resize_keyboard=True
)