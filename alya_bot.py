
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from gtts import gTTS
import os, random, subprocess
import whisper

API_ID = int(os.environ.get("API_ID", "27240578"))
API_HASH = os.environ.get("API_HASH", "5dc3831cf1f862ee7aabfc16c750fc89")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7336757348:AAEcBMf1G7Xo6j6DzhzhIPyIJoZ4YaBc1jc")

app = Client("alya_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
model = whisper.load_model("base")
sohbet_modlari = {}
aktif_oyun = {}
kelimeler = ["python", "telegram", "pyrogram", "bot", "kodlama"]

def ana_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Etiketle", callback_data="etiket")],
        [InlineKeyboardButton("Sohbet Aç", callback_data="sohbet_ac"),
         InlineKeyboardButton("Sohbet Kapat", callback_data="sohbet_kapat")],
        [InlineKeyboardButton("TTS", callback_data="tts")],
        [InlineKeyboardButton("STT", callback_data="stt")],
        [InlineKeyboardButton("Taş-Kağıt-Makas", callback_data="tkm")],
        [InlineKeyboardButton("Zar At", callback_data="zar")],
        [InlineKeyboardButton("Kelime Oyunu", callback_data="kelime")],
        [InlineKeyboardButton("Yardım", callback_data="yardim")]
    ])

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Alya'ya hoş geldin!", reply_markup=ana_menu())

@app.on_callback_query()
async def cb(client, cb: CallbackQuery):
    chat_id = cb.message.chat.id
    data = cb.data
    if data == "etiket":
        tags = []
        async for m in client.get_chat_members(chat_id):
            if not m.user.is_bot:
                tags.append(m.user.mention)
        text = "\n".join([" ".join(tags[i:i+5]) for i in range(0, len(tags), 5)])
        await cb.message.edit_text(text or "Kimse bulunamadı.")
    elif data == "sohbet_ac":
        sohbet_modlari[chat_id] = True
        await cb.message.edit_text("Sohbet modu açıldı.")
    elif data == "sohbet_kapat":
        sohbet_modlari[chat_id] = False
        await cb.message.edit_text("Sohbet modu kapatıldı.")
    elif data == "tts":
        await cb.message.edit_text("Kullanım: /konus Merhaba dünya")
    elif data == "stt":
        await cb.message.edit_text("Sesli mesaja yanıt olarak /stt yaz.")
    elif data == "tkm":
        await cb.message.edit_text("Komut: /oyun_tkm taş | kağıt | makas")
    elif data == "zar":
        await cb.message.edit_text(f"Zar: {random.randint(1,6)}")
    elif data == "kelime":
        kelime = random.choice(kelimeler)
        aktif_oyun[chat_id] = kelime
        karisik = ''.join(random.sample(kelime, len(kelime)))
        await cb.message.edit_text(f"Harfleri sırala: {karisik}")
    elif data == "yardim":
        await cb.message.edit_text("/konus, /stt, /oyun_tkm, /zar\nEtiket için butonu kullan.")

@app.on_message(filters.command("konus"))
async def konus(client, message):
    if len(message.command) < 2:
        return await message.reply("Kullanım: /konus <metin>")
    metin = message.text.split(" ", 1)[1]
    tts = gTTS(metin, lang="tr")
    tts.save("tts.mp3")
    await message.reply_voice("tts.mp3")
    os.remove("tts.mp3")

@app.on_message(filters.command("stt") & filters.reply & filters.voice)
async def stt(client, message):
    try:
        file = await message.reply_to_message.download()
        subprocess.run(["ffmpeg", "-i", file, "out.wav"], check=True)
        result = model.transcribe("out.wav", language="tr")
        await message.reply(result["text"])
        os.remove(file); os.remove("out.wav")
    except Exception as e:
        await message.reply(f"Hata: {e}")

@app.on_message(filters.command("oyun_tkm"))
async def oyun(client, message):
    secim = message.command[1].lower()
    bot = random.choice(["taş", "kağıt", "makas"])
    sonuc = "Berabere!"
    if (secim == "taş" and bot == "makas") or (secim == "kağıt" and bot == "taş") or (secim == "makas" and bot == "kağıt"):
        sonuc = "Kazandın!"
    elif secim != bot:
        sonuc = "Bot kazandı!"
    await message.reply(f"Sen: {secim}\nBot: {bot}\n{sonuc}")

@app.on_message(filters.text)
async def kelime_tahmin(client, message):
    chat_id = message.chat.id
    if chat_id in aktif_oyun:
        if message.text.lower().strip() == aktif_oyun[chat_id]:
            await message.reply("Doğru bildin! 🎉")
            aktif_oyun.pop(chat_id)
        else:
            await message.reply("Yanlış, tekrar dene.")

app.run()
