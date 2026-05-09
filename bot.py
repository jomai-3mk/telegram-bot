from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

print("BOT STARTING...")

# التوكن الصحيح من Environment Variables
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN is missing! Set it in Render Environment Variables")

print("TOKEN LOADED")

teachers = set()
students = set()

keyboard = ReplyKeyboardMarkup(
    [
        ["🚻", "🍔"],
        ["💧", "🆘"]
    ],
    resize_keyboard=True
)

message_map = {
    "🚻": "الطالب يريد الذهاب للحمام",
    "🍔": "الطالب جائع",
    "💧": "الطالب يريد ماء",
    "🆘": "الطالب يحتاج مساعدة"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    students.add(user_id)
    teachers.discard(user_id)

    await update.message.reply_text(
        "اختر الحالة:",
        reply_markup=keyboard
    )

async def teacher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    teachers.add(user_id)
    students.discard(user_id)

    await update.message.reply_text("تم تسجيلك كمدرس")

async def student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    students.add(user_id)
    teachers.discard(user_id)

    await update.message.reply_text("تم تحويلك إلى طالب")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_chat.id

    if text in message_map:

        if user_id in teachers:
            await update.message.reply_text("أنت مدرس لا ترسل طلبات")
            return

        msg = message_map[text]

        for teacher_id in teachers:
            await context.bot.send_message(
                chat_id=teacher_id,
                text=msg
            )

        await update.message.reply_text("تم إرسال الطلب")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("teacher", teacher))
    app.add_handler(CommandHandler("student", student))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("RUNNING BOT...")
    app.run_polling()


if __name__ == "__main__":
    main()