# menu_ai.py
from google import genai
from telebot import types

# ================= KONFIGURASI =================
# Ganti bagian dalam tanda kutip dengan API Key Gemini kamu
GEMINI_API_KEY = "AQ.Ab8RN6JbWqJJxr42ty6o6fl0CZo0OsQCTAUXx6Vk56e55lZ0uQ"

client = genai.Client(api_key=GEMINI_API_KEY)
# ===============================================

def register(bot):
    @bot.message_handler(commands=['ai'])
    def menu_ai(message):
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

    @bot.callback_query_handler(func=lambda call: call.data.startswith('ai_'))
    def callback_ai(call):
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

    @bot.message_handler(commands=['tanya'])
    def tanya_ai(message):
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

    print("[✓] Menu AI berhasil didaftarkan.")
