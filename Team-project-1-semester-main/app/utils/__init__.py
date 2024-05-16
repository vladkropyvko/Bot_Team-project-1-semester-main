from aiogram.types import Message, CallbackQuery
from typing import Union


async def edit_or_answer_photo(message: Union[Message, CallbackQuery], photo_id:int, text: str, keyboard=None, *args, **kwargs):
    if isinstance(message, CallbackQuery):
        msg = message.message
    
    await msg.answer_photo(photo_id, caption=text, reply_markup=keyboard, **kwargs)
    if msg.from_user.is_bot:
        await msg.delete()
        

async def edit_or_answer(message: Union[Message, CallbackQuery], text: str, keyboard=None, *args, **kwargs):
    if isinstance(message, CallbackQuery):
        await message.message.answer(text=text, reply_markup=keyboard, **kwargs)
        await message.message.delete()
    else:
        if message.from_user.is_bot:
            await message.edit_text(text=text, reply_markup=keyboard, **kwargs)
        else:
            await message.answer(text=text, reply_markup=keyboard, **kwargs)
