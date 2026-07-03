from aiogram.types import Message

from ORION.keyboards.main import main_kb

async def start(message: Message):
    await message.answer(
        "Вас приветствует индивидуальный инвестиционный бот <b>ORION</b>\n\n"
        "Выберите действие:",
        reply_markup=main_kb
    )