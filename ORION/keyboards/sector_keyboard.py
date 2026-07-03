from aiogram.utils.keyboard import InlineKeyboardBuilder


def sectors_keyboard(sectors):

    builder = InlineKeyboardBuilder()

    for sector, name in sectors:
        builder.button(
            text=name,
            callback_data=f"sector:{sector}"
        )

    builder.adjust(2)

    return builder.as_markup()



def sector_back_keyboard():

    builder = InlineKeyboardBuilder()

    builder.button(
        text="⬅️ Назад",
        callback_data="back_to_sectors"
    )

    return builder.as_markup()