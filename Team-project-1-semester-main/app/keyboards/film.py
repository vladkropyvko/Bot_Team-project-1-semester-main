from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.data.handler import get_films


def build_films_keyboard(films: list):
    builder = InlineKeyboardBuilder()
    for index, film in enumerate(films):
        builder.button(text=film.get("title"), callback_data=f"film_{index}")
    return builder.as_markup()

def build_film_details_keyboard(film, film_id):
    builder = InlineKeyboardBuilder()
    if film_id > 0:
        builder.button(text="Önceki", callback_data=f"film_{film_id-1}")
    builder.button(text="Bağlantıya gitmek", url=film.get("url"))
    builder.button(text="Go back", callback_data="back")
    if film_id < len(get_films()) - 1:
        builder.button(text="Sonraki", callback_data=f"film_{film_id+1}")
    return builder.as_markup()
    

def build_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Go back", callback_data="back")
    return builder.as_markup()