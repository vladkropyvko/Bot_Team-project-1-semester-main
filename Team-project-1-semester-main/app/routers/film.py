from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from typing import BinaryIO, Union
from aiogram.utils.markdown import hbold

from .. utils import edit_or_answer, edit_or_answer_photo
from .. data import get_films, get_film, save_film
from .. fsm import FilmCreateForm
from .. keyboards import (build_films_keyboard,
                         build_menu_keyboard, build_film_details_keyboard,)


film_router = Router()




@film_router.message(Command("films"))
@film_router.callback_query(F.data == "films")
@film_router.message(F.text.casefold() == "films")
async def show_films_command(message: Union[Message, CallbackQuery], state: FSMContext) -> None:
    films = get_films()
    if isinstance(message, Message):
        if films:
            keyboard = build_films_keyboard(films)
            await edit_or_answer(message, "Herhangi bir filmi seçin", keyboard)
        else:
            await edit_or_answer(message, "Maalesef şu anda filmler yok. Yeni bir tane oluşturmak için /filmcreate komutunu deneyin.", ReplyKeyboardRemove())
    elif isinstance(message, CallbackQuery):
        if films:
            keyboard = build_films_keyboard(films)
            await edit_or_answer(message.message, "Herhangi bir film seçin", keyboard)
        else:
            await edit_or_answer(message.message, "Üzgünüz, şu anda filmler yok. Yeni bir tane oluşturmak için /filmcreate komutunu deneyin.")

@film_router.callback_query(F.data.startswith("film_"))
async def show_film_details(callback: CallbackQuery, state: FSMContext) -> None:
    film_id = int(callback.data.split("_")[-1])
    film = get_film(film_id)
    text = f"Назва:{hbold(film.get('title'))}\nAçıklama:{hbold(film.get('desc'))}\nPuan:{hbold(film.get('rating'))}"
    photo_id = film.get('photo')
    url = film.get('url')
    await edit_or_answer_photo(callback, photo_id, text, keyboard=build_film_details_keyboard(film, film_id))
    # await callback.message.answer_photo()
    # await edit_or_answer(callback.message, text, build_film_details_keyboard(url))


@film_router.message(Command("filmcreate"))
@film_router.callback_query(F.data == "filmcreate")
@film_router.message(F.text.casefold() == "filmcreate")
@film_router.message(F.text.casefold() == "create film")
async def create_film_command(message: Union[Message, CallbackQuery], state: FSMContext) -> None:
    await state.clear()
    await state.set_state(FilmCreateForm.title)
    await edit_or_answer(message, "Film adı nedir?", ReplyKeyboardRemove())


@film_router.message(FilmCreateForm.title)
async def procees_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(FilmCreateForm.desc)
    await edit_or_answer(message, "Film hakkında nasıl bir açıklama?", ReplyKeyboardRemove())


@film_router.message(FilmCreateForm.desc)
async def procees_desctription(message: Message, state: FSMContext) -> None:
    data = await state.update_data(desc=message.text)
    await state.set_state(FilmCreateForm.url)
    await edit_or_answer(
        message,
        f"Filmin bağlantısını sağlayın: {hbold(data.get('title'))}",
        ReplyKeyboardRemove(),
    )


@film_router.message(FilmCreateForm.url)
@film_router.message(F.text.contains('http'))
async def procees_url(message: Message, state: FSMContext) -> None:
    data = await state.update_data(url=message.text)
    await state.set_state(FilmCreateForm.photo)
    await edit_or_answer(
        message,
        f"Film afişi için bir fotoğraf sağlayın: {hbold(data.get('title'))}",
        ReplyKeyboardRemove(),
    )


@film_router.message(FilmCreateForm.photo)
@film_router.message(F.photo)
async def procees_photo_binary(message: Message, state: FSMContext) -> None:
    photo = message.photo[-1]
    photo_id = photo.file_id

    data = await state.update_data(photo=photo_id)
    await state.set_state(FilmCreateForm.rating)
    await edit_or_answer(
        message,
        f"Filmin puanını belirtin: {hbold(data.get('title'))}",
        ReplyKeyboardRemove(),
    )


@film_router.message(FilmCreateForm.rating)
async def procees_rating(message: Message, state: FSMContext) -> None:
    data = await state.update_data(rating=message.text)
    await state.clear()
    save_film(data)
    return await show_films_command(message, state)


