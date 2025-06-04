import os
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from gtts import gTTS

API_ID = int(os.environ.get("API_ID", "27240578"))
API_HASH = os.environ.get("API_HASH", "5dc3831cf1f862ee7aabfc16c750fc89")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7336757348:AAEcBMf1G7Xo6j6DzhzhIPyIJoZ4YaBc1jc")

if not all([API_ID, API_HASH, BOT_TOKEN]):
    raise ValueError("API_ID, API_HASH ve BOT_TOKEN ortam değişkenleri ayarlanmalı!")

bot = Client("alya", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
chat_mode = {}

@bot.on_message(filters.command("start"))
async def start(client, message):
    buttons = [[
        InlineKeyboardButton("🗣 TTS", callback_data="tts"),
        InlineKeyboardButton("🎙 STT", callback_data="stt")
    ],[
        InlineKeyboardButton("👥 Etiketle", callback_data="tag"),
        InlineKeyboardButton("💬 Sohbet Modu", callback_data="chat"),
        InlineKeyboardButton("🎮 Oyun", callback_data="game")
    ]]
    await message.reply("Merhaba! Ben Alya. Ne yapmak istersin?", reply_markup=InlineKeyboardMarkup(buttons))

@bot.on_callback_query()
async def callbacks(client, callback_query):
    data = callback_query.data
    if data == "tts":
        await callback_query.message.reply("Metni /tts [mesaj] şeklinde gönder.")
    elif data == "stt":
        await callback_query.message.reply("Bir ses dosyası gönder, yazıya dökeyim.")
    elif data == "tag":
        await callback_query.message.reply("Grup içinde /tagall yaz, herkesi etiketleyeyim.")
    elif data == "chat":
        await callback_query.message.reply("Sohbet modu aktif! Mesaj gönder.")
        chat_mode[callback_query.message.chat.id] = True
    elif data == "game":
        number = random.randint(1, 10)
        await callback_query.message.reply(f"🎲 Tahmin et! 1 ile 10 arasında bir sayı tuttum. /tahmin [sayı]")

@bot.on_message(filters.command("tts"))
async def tts(client, message):
    if len(message.command) < 2:
        return await message.reply("Lütfen metin gir: /tts Merhaba!")
    text = message.text.split(" ", 1)[1]
    tts = gTTS(text, lang="tr")
    tts.save("voice.mp3")
    await message.reply_voice("voice.mp3")

@bot.on_message(filters.voice)
async def stt(client, message):
    await message.reply("🛑 Ses tanıma (STT) şu anda desteklenmiyor.")

@bot.on_message(filters.command("tagall") & filters.group)
async def tag_all(client, message):
    members = [f"@{member.user.username}" for member in await client.get_chat_members(message.chat.id) if member.user.username]
    chunks = [members[i:i + 5] for i in range(0, len(members), 5)]
    for group in chunks:
        await message.reply(" ".join(group))

@bot.on_message(filters.command("tahmin"))
async def guess(client, message):
    try:
        number = int(message.command[1])
        correct = random.randint(1, 10)
        if number == correct:
            await message.reply("🎉 Doğru tahmin!")
        else:
            await message.reply(f"❌ Yanlış! Ben {correct} demiştim.")
    except:
        await message.reply("Kullanım: /tahmin [1-10 arası sayı]")

@bot.on_message(filters.text & filters.private)
async def chat_mode_handler(client, message):
    if chat_mode.get(message.chat.id):
        await message.reply("🧠 Şu an sohbet modundayız. (Bu demo moddur.)")

bot.run()