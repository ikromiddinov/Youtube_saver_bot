import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Professional yuklash sozlamalari
YDL_OPTIONS = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'max_filesize': 50 * 1024 * 1024, # 50MB Telegram bepul limiti
    'quiet': True,
    'no_warnings': True,
    # YouTube cheklovlarini chetlab o'tish uchun "Fake User Agent"
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'referer': 'https://www.google.com/',
}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Professional Downloader Botga xush kelibsiz! \n\nLink yuboring (YouTube, Instagram, TikTok)")

@dp.message()
async def handle_docs(message: types.Message):
    url = message.text
    if not (url.startswith("http")):
        return

    status_msg = await message.answer("⏳ Video tahlil qilinmoqda...")
    
    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            
            video = types.FSInputFile(file_path)
            await status_msg.edit_text("📤 Video yuborilmoqda...")
            await bot.send_video(message.chat.id, video, caption=f"✅ Yuklab olindi: {info.get('title', 'Video')}")
            
            # Faylni serverdan o'chirish (joy band qilmasligi uchun)
            if os.path.exists(file_path):
                os.remove(file_path)
            await status_msg.delete()

    except Exception as e:
        error_text = str(e)
        if "Sign in" in error_text:
            await status_msg.edit_text("❌ YouTube hozircha bu serverni chekladi. Boshqa platformalarni (TikTok/Instagram) sinab ko'ring.")
        else:
            await status_msg.edit_text(f"❌ Xatolik: {error_text[:100]}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
