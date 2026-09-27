# menu_ai.py
from google import genai
from telebot import types

# ================= KONFIGURASI =================
GEMINI_API_KEY = "AQ.Ab8RN6L15Q2YbZSzSOSPJSrw80lAad2GtNnDoiiqMx4bgHVZzA"
client = genai.Client(api_key=GEMINI_API_KEY)
# ===============================================

# WAJIB ADA — ini yang bikin bot bisa register plugin
MENU_NAME = "🤖 Menu AI"
MENU_COMMAND = "ai"
MENU_DESCRIPTION = "Tanya jawab dengan Gemini AI"

def handle(bot, message):
    """Fungsi utama yang dipanggil bot saat user ketik /ai"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("💬 Tanya AI", callback_data="ai_tanya")
    btn2 = types.InlineKeyboardButton("🖼️ Buat Gambar", callback_data="ai_gambar")
    btn3 = types.InlineKeyboardButton("📝 Ringkas Teks", callback_data="ai_ringkas")
    btn4 = types.InlineKeyboardButton("❌ Tutup", callback_data="ai_tutup")
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(
        message.chat.id,
        "🤖 *Menu AI*\nSilakan pilih fitur yang ingin kamu gunakan:",
        parse_mode="Markdown",
        reply_markup=markup
    )

def callback(bot, call):
    """Fungsi buat handle tombol yang diklik"""
    if call.data == "ai_tanya":
        bot.answer_callback_query(call.id, "Kirim pertanyaanmu dengan format: /tanya <teks>")
        bot.send_message(call.message.chat.id, "Contoh: `/tanya Apa itu Python?`", parse_mode="Markdown")

    elif call.data == "ai_gambar":
        bot.answer_callback_query(call.id, "Fitur gambar segera hadir!")

    elif call.data == "ai_ringkas":
        bot.answer_callback_query(call.id, "Kirim teks yang mau diringkas.")
        bot.send_message(call.message.chat.id, "Kirim teks panjangmu, nanti AI akan meringkasnya.")

    elif call.data == "ai_tutup":
        bot.delete_message(call.message.chat.id, call.message.message_id)

def tanya(bot, message):
    """Fungsi buat handle /tanya"""
    pertanyaan = message.text.replace('/tanya', '').strip()
    if not pertanyaan:
        bot.reply_to(message, "❌ Kamu belum memasukkan pertanyaan.\nContoh: `/tanya Apa itu AI?`", parse_mode="Markdown")
        return

    bot.reply_to(message, "⏳ Sedang berpikir...")

    try:
        interaction = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=pertanyaan,
        )
        hasil = interaction.text
        bot.reply_to(message, f"🤖 *Jawaban AI:*\n\n{hasil}", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Terjadi kesalahan: {str(e)}")
