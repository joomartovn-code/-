# Telegram Translator Bot with Inline Buttons (python-telegram-bot v20+)

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from googletrans import Translator
import os

# ------------------ CONFIG ------------------
TOKEN = '8466913325:AAG-YQeTQr_D29ea90zd6WBOeMUNmuRL7f4'  # <= вставь токен сюда
# ---------------------------------------------

translator = Translator()

# Сохраняем язык для каждого пользователя
def get_lang(context: ContextTypes.DEFAULT_TYPE):
    return context.user_data.get("lang", "en")  # по умолчанию переводим на English

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("🇬🇧 English", callback_data="en"),
        InlineKeyboardButton("🇷🇺 Russian", callback_data="ru"),
        InlineKeyboardButton("🇰🇿 Kazakh", callback_data="kk"),
    ]]

    await update.message.reply_text(
        "🌍 Привет! Я бот-переводчик. Выбери язык, на который буду переводить:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = query.data
    context.user_data["lang"] = lang

    await query.edit_message_text(f"✅ Язык перевода установлен: {lang.upper()}\nНапиши текст, и я переведу.")

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(context)
    text = update.message.text

    try:
        result = translator.translate(text, dest=lang)
        await update.message.reply_text(f"🌐 Перевод ({lang.upper()}):\n{result.text}")
    except Exception as e:
        await update.message.reply_text("⚠️ Ошибка перевода, попробуй ещё раз.")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()