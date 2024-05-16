from dotenv import load_dotenv
from os import getenv

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from . routers import default_router, film_router

# Varsayılan olarak .env dosyasından çevre değişkenlerini yüklüyoruz.
load_dotenv()


# Tüm işleyicileri Router veya Dispatcher atamak iyi bir uygulama olabilir.
root_router = Router()
root_router.include_routers(default_router, film_router, )

# Kullanıcının kullanabileceği tüm komutların kurulması
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Botu başlatır"),
        BotCommand(command="help", description="Komutların listesini alır"),
        BotCommand(command="filmcreate", description="Yeni bir film oluşturur"),
        BotCommand(command="clear", description="Son mesajları siler"),
        BotCommand(command="films", description="Filmleri seçer"),
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    # Botun belirteci çevreden alınacak
    TOKEN = getenv("BOT_TOKEN")
    # Bot nesnesi oluşturalım
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    
    dp = Dispatcher()
    dp.include_router(root_router)
    # Komutları kurma işlevini başlatma
    await set_commands(bot)

    # Bot için olayları işlemeye başlayalım.
    await dp.start_polling(bot)


