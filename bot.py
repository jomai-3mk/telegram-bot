from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8740241159:AAEUJh_5NK2OrHbWhSvnPmIHk1Wcv9d7-eo"

teachers = set()
students = set()

# الأزرار (إيموجيات)
keyboard = ReplyKeyboardMarkup([
    ["🚻", "🍔"],
    ["💧", "🆘"]
], resize_keyboard=True)

# رسائل لكل إيموجي
message_map = {
    "🚻": "الطالب يريد الذهاب للحمام",
    "🍔": "الطالب جائع",
    "💧": "الطالب يريد ماء",
    "🆘": "الطالب يحتاج مساعدة"
}

# بدء البوت (طالب)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    students.add(user_id)
    teachers.discard(user_id)

    await update.message.reply_text(
        "اختر الحالة:",
        reply_markup=keyboard
    )

# تسجيل مدرس
async def teacher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    teachers.add(user_id)
    students.discard(user_id)

    await update.message.reply_text("تم تسجيلك كمدرس")

# تحويل إلى طالب مرة ثانية
async def student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    teachers.discard(user_id)
    students.add(user_id)

    await update.message.reply_text("تم تحويلك إلى طالب")

# استقبال الضغط على الأزرار
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_chat.id

    if text in message_map:

        # يمنع المدرس من إرسال طلبات بالغلط
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

# تشغيل التطبيق
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("teacher", teacher))
app.add_handler(CommandHandler("student", student))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()