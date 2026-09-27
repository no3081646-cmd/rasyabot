# menu_ai.py
from google import genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# ================= KONFIGURASI =================
GEMINI_API_KEY = "AQ.Ab8RN6L15Q2YbZSzSOSPJSrw80lAad2GtNnDoiiqMx4bgHVZzA"
client = genai.Client(api_key=GEMINI_API_KEY)
# ===============================================

# ================= WAJIB ADA =================
MENU_NAME = "🤖 Menu AI"
MENU_ORDER = 4
MENU_CALLBACK = "menu_ai"
# =============================================

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💬 Tanya AI", callback_data="ai_tanya"),
         InlineKeyboardButton("🖼️ Buat Gambar", callback_data="ai_gambar")],
        [InlineKeyboardButton("📝 Ringkas Teks", callback_data="ai_ringkas"),
         InlineKeyboardButton("❌ Tutup", callback_data="ai_tutup")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 *Menu AI*\nSilakan pilih fitur yang ingin kamu gunakan:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "ai_tanya":
        await query.message.reply_text("Kirim: `/tanya Apa itu Python?`", parse_mode="Markdown")
    elif query.data == "ai_gambar":
        await query.message.reply_text("🚧 Fitur gambar segera hadir!")
    elif query.data == "ai_ringkas":
        await query.message.reply_text("Kirim teks panjangmu, nanti AI meringkasnya.")
    elif query.data == "ai_tutup":
        await query.message.delete()

async def tanya_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pertanyaan = " ".join(context.args) if context.args else ""
    if not pertanyaan:
        await update.message.reply_text("❌ Contoh: `/tanya Apa itu AI?`", parse_mode="Markdown")
        return

    tunggu = await update.message.reply_text("⏳ Sedang berpikir...")
    try:
        interaction = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=pertanyaan,
        )
        await tunggu.delete()
        await update.message.reply_text(f"🤖 *Jawaban AI:*\n\n{interaction.text}", parse_mode="Markdown")
    except Exception as e:
        await tunggu.edit_text(f"❌ Error: {str(e)}")
