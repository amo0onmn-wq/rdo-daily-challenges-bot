# main.py
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config import TELEGRAM_TOKEN, KEYWORDS_MAP, ARABIC_ROLE_TITLES
from rdo_client import fetch_challenges
from formatting import format_single_group, format_full_all

# إعداد اللوق
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ======= دوال مساعدة =======

def _build_main_keyboard() -> InlineKeyboardMarkup:
    """أزرار رئيسية لعرض أنواع التحديات."""
    keyboard = [
        [
            InlineKeyboardButton("📋 التحديات العامة", callback_data="show_general"),
        ],
        [
            InlineKeyboardButton("🎯 تحديات الباونتي", callback_data="show_bounty"),
            InlineKeyboardButton("📦 تحديات التاجر", callback_data="show_trader"),
        ],
        [
            InlineKeyboardButton("🗺️ تحديات الكولكتر", callback_data="show_collector"),
        ],
        [
            InlineKeyboardButton("🍺 تحديات المونشاينر", callback_data="show_moonshiner"),
            InlineKeyboardButton("🌿 تحديات الطبيعة", callback_data="show_naturalist"),
        ],
        [
            InlineKeyboardButton("🔥 عرض كل التحديات", callback_data="show_all"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


async def _send_group(role_key: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """يرسل قسم معيّن (عام / تاجر / ...)."""
    groups = fetch_challenges()
    items = groups.get(role_key, [])
    text = format_single_group(role_key, items)

    chat_id = (
        update.effective_chat.id
        if update.effective_chat
        else None
    )
    if not chat_id:
        return

    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
    )


# ======= أوامر البوت =======

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "أهلًا بك في بوت *تحديات Red Dead Online* 🎮🤠\n\n"
        "اختَر من الأزرار بالأسفل لعرض نوع التحديات اللي تبيه، "
        "أو استخدم الأوامر:\n"
        "- `/challenges` : عرض كل التحديات (عام + أدوار)\n"
        "- `/general` : التحديات العامة\n"
        "- `/bounty` : تحديات الباونتي\n"
        "- `/trader` : تحديات التاجر\n"
        "- `/collector` : تحديات الكولكتر\n"
        "- `/moonshiner` : تحديات المونشاينر\n"
        "- `/naturalist` : تحديات الطبيعة\n\n"
        "تقدّر بعد تكتب كلمات مثل:\n"
        "`التحديات`, `تحديات التاجر`, `تحديات الكولكتر` ... والبوت يفهمها 😉"
    )
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=_build_main_keyboard(),
    )


async def cmd_challenges(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض كل التحديات (عام + أدوار)."""
    groups = fetch_challenges()
    text = format_full_all(groups)
    await update.message.reply_text(text, parse_mode="Markdown")


async def cmd_general(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send_group("general", update, context)


async def cmd_bounty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send_group("bounty", update, context)


async def cmd_trader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send_group("trader", update, context)


async def cmd_collector(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send_group("collector", update, context)


async def cmd_moonshiner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send_group("moonshiner", update, context)


async def cmd_naturalist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _send_group("naturalist", update, context)


# ======= أزرار الـ Inline =======

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    fake_update = Update(update.update_id, message=query.message)

    if data == "show_general":
        await cmd_general(fake_update, context)
    elif data == "show_bounty":
        await cmd_bounty(fake_update, context)
    elif data == "show_trader":
        await cmd_trader(fake_update, context)
    elif data == "show_collector":
        await cmd_collector(fake_update, context)
    elif data == "show_moonshiner":
        await cmd_moonshiner(fake_update, context)
    elif data == "show_naturalist":
        await cmd_naturalist(fake_update, context)
    elif data == "show_all":
        await cmd_challenges(fake_update, context)
    else:
        await query.edit_message_text("زر غير معروف 🤔")


# ======= التعامل مع الرسائل النصية (الكلمات المفتاحية) =======

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    # نشتغل على نسخة بدون فراغات عشان نتحمل اختلاف بسيط بالكتابة
    normalized = text.replace(" ", "")

    # نحاول نربط الكلمة المفتاحية بالقسم المناسب
    for role_key, phrases in KEYWORDS_MAP.items():
        for phrase in phrases:
            p_norm = phrase.replace(" ", "")
            if p_norm and p_norm in normalized:
                # وجدنا مطابق
                await _send_group(role_key, update, context)
                return

    # لو ما تعرفنا على الكلمة، نساعد المستخدم
    tips = (
        "ما فهمت طلبك 🤔\n\n"
        "تقدّر تكتب مثلاً:\n"
        "- `التحديات`\n"
        "- `تحديات التاجر`\n"
        "- `تحديات الكولكتر`\n"
        "- `تحديات المونشاينر`\n"
        "- `تحديات الطبيعة`\n"
        "- `تحديات الباونتي`\n"
        "أو استخدم الأمر `/challenges` لعرض كل التحديات."
    )
    await update.message.reply_text(tips, parse_mode="Markdown")


# ======= هاندلر للأخطاء =======

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Exception while handling update:", exc_info=context.error)


# ======= نقطة التشغيل الرئيسية =======

def main():
    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "YOUR_BOT_TOKEN_HERE":
        raise RuntimeError("رجاءً ضعي توكن البوت في متغير البيئة BOT_TOKEN أو في config.py")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # أوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("challenges", cmd_challenges))
    app.add_handler(CommandHandler("general", cmd_general))
    app.add_handler(CommandHandler("bounty", cmd_bounty))
    app.add_handler(CommandHandler("trader", cmd_trader))
    app.add_handler(CommandHandler("collector", cmd_collector))
    app.add_handler(CommandHandler("moonshiner", cmd_moonshiner))
    app.add_handler(CommandHandler("naturalist", cmd_naturalist))

    # أزرار
    app.add_handler(CallbackQueryHandler(button_handler))

    # أي نص عادي
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # أخطاء
    app.add_error_handler(error_handler)

    print("RDO Daily Challenges bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
