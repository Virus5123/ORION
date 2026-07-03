from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def accounts_keyboard(accounts):

    buttons = []

    for i, account in enumerate(accounts, start=1):
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"№{i} {account.name}",
                    callback_data=f"account_{account.id}"
                )
            ]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text="🌍 Общий портфель",
                callback_data="total_portfolio"
            )
        ]
    )
    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

def back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="back_accounts"
                )
            ]
        ]
    )