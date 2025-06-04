import os
from pyrogram import Client, filters
import gtts
import whisper
import ffmpeg

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not all([API_ID, API_HASH, BOT_TOKEN]):
    raise ValueError("API_ID, API_HASH ve BOT_TOKEN ortam değişkenleri ayarlanmalı!")

bot = Client("alya", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

model = whisper.load_model("base")

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Merhaba! Ben Alya. Sohbet edebilirim, sesleri metne çevirebilirim ve daha fazlası!")

bot.run()
