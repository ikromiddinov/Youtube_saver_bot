import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import yt_dlp

# Tokenni Render-dagi Environment Variables-dan oladi
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Assalomu alaykum! YouTube linkini yuboring, men uni yuklab beraman.")

@dp.message()
async def download_video(message: types.Message):
    if "youtube.com" in message.text or "youtu.be" in message.text:
        msg = await message.answer("Video yuklanmoqda, kuting...")
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': 'video.mp4',
                'max_filesize': 50 * 1024 * 1024,
                'quiet': True,
                'no_warnings': True,
                # Quyidagi qatorlarni qo'shing:
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'referer': 'https://www.google.com/',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([message.text])
            
            video = types.FSInputFile("video.mp4")
            await bot.send_video(message.chat.id, video)
            os.remove("video.mp4")
            await msg.delete()
        except Exception as e:
            await message.answer(f"Xatolik yuz berdi: {str(e)}")
    else:
        await message.answer("Iltimos, to'g'ri YouTube linkini yuboring.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
