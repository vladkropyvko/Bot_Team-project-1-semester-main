from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="Film listesi", callback_data=f"films")
    builder.button(text="Yeni bir film eklemek", callback_data=f"filmcreate")

    return builder.as_markup()

