"""
معالجات أوامر ورسائل البوت
يمنع الإرسال والتفاعل العشوائي في الخاص ويوجه الزوار إلى القناة الرسمية، مع لوحة تحكم حصرية للأدمن
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import (
    get_channel_id,
    set_channel_id,
    get_channel_link,
    set_channel_link,
    get_admin_ids,
    add_admin_id,
    get_quran_pages_per_day,
    set_quran_pages_per_day
)
from services.quran_service import (
    load_state,
    set_current_page,
    get_daily_wird_pages,
    advance_wird_state
)
from services.prayer_times import get_makkah_prayer_times, ARABIC_PRAYER_NAMES
from services.formatter import (
    format_prayer_table_post,
    format_adhkar_sabah_post,
    format_adhkar_masa_post,
    format_adhkar_nawm_post,
    format_witr_reminder,
    format_azan_reminder,
    format_friday_kahf_post,
    format_friday_salawat_post,
    format_friday_istijaba_post,
    format_daily_dua_post
)
from data.adhkar_sabah import ADHKAR_SABAH
from data.adhkar_masa import ADHKAR_MASA
from data.adhkar_nawm import ADHKAR_NAWM
from data.witr import WITR_REMINDERS
from data.friday import FRIDAY_REMINDERS
from data.authentic_duas import AUTHENTIC_DUAS
from bot.sender import send_channel_message, send_channel_quran_pages

logger = logging.getLogger(__name__)

def is_admin(user_id: int) -> bool:
    """التحقق مما إذا كان المستخدم مديراً للبوت"""
    admins = get_admin_ids()
    if not admins:
        # إذا لم يتم تعيين أي أدمن بعد، يصبح أول مستخدم يتواصل مع البوت أدمن تلقائياً
        add_admin_id(user_id)
        return True
    return user_id in admins

async def handle_private_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    التعامل مع الرسائل الخاصة:
    إذا كان المستخدم عادياً، يوجهه بلطف إلى القناة الرسمية فقط ولا ينشر له في الخاص.
    """
    if not update.effective_user or not update.message:
        return
        
    user_id = update.effective_user.id
    
    # إذا لم يكن أدمن
    if not is_admin(user_id):
        channel_link = get_channel_link()
        channel_id = get_channel_id()
        channel_title = channel_id if channel_id else "قناتنا الرسمية"
        
        reply_text = (
            "<b>السلام عليكم ورحمة الله وبركاته 🌸</b>\n\n"
            "هذا البوت المبارك مخصص للبث اليومي في <b>القناة الرسمية فقط</b>.\n"
            "يتم من خلالها نشر:\n"
            "▫️ الورد اليومي من مصحف مجمع الملك فهد الشريف بالمدينة المنورة.\n"
            "▫️ أذكار الصباح والمساء وأذكار النوم الصحيحة.\n"
            "▫️ تذكير صلاة الوتر واستغفار الأسحار.\n"
            "▫️ مواقيت الصلاة والأذان بتوقيت مكة المكرمة (تقويم أم القرى).\n\n"
            f"👇 <b>تفضل بالانضمام للقناة لمتابعة كل جديد:</b>\n"
            f"🔗 <a href='{channel_link}'>{channel_title}</a>"
        )
        await update.message.reply_text(
            reply_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        return

    # إذا كان أدمن ولم يكتب أمراً معروفاً، نعرض له لوحة التحكم
    await cmd_start(update, context)

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لوحة تحكم الأدمن لإدارة البوت وفحص المنشورات"""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return await handle_private_message(update, context)

    channel_id = get_channel_id() or "⚠️ لم تُحدد بعد"
    state = load_state()
    curr_page = state.get("current_page", 1)
    khatmat = state.get("khatmah_count", 0)
    pages_day = get_quran_pages_per_day()

    msg = (
        "<b>🕋 مرحباً بك في لوحة تحكم بوت الأذكار والقرآن الكريم 🕋</b>\n"
        "<i>﴿ خادم الورد القرآني والأذكار ومواقيت مكة المكرمة ﴾</i>\n\n"
        "<b>⚙️ الإعدادات الحالية:</b>\n"
        f"📢 <b>القناة المستهدفة:</b> <code>{channel_id}</code>\n"
        f"📖 <b>الصفحة الحالية من المصحف:</b> {curr_page} / 604\n"
        f"🏆 <b>عدد الختمات المنجزة:</b> {khatmat}\n"
        f"📄 <b>معدل الصفحات اليومية:</b> {pages_day} صفحة\n\n"
        "<b>🛠️ أوامر التحكم السريع:</b>\n"
        "▫️ <code>/setchannel @YourChannel</code> — تعيين معرف القناة\n"
        "▫️ <code>/setlink https://t.me/...</code> — تعيين رابط الانضمام للقناة\n"
        "▫️ <code>/setpage 50</code> — تغيير صفحة البداية للقرآن الكريم\n"
        "▫️ <code>/setrate 2</code> — تحديد عدد صفحات القرآن باليوم (1 إلى 10)\n"
        "▫️ <code>/status</code> — تقرير شامل عن حالة البوت والمواقيت\n\n"
        "<b>🧪 تجربة النشر الفوري بالقناة (Test):</b>\n"
        "▫️ /test_quran — إرسال ورد القرآن الآن\n"
        "▫️ /test_sabah — إرسال أذكار الصباح\n"
        "▫️ /test_masa — إرسال أذكار المساء\n"
        "▫️ /test_witr — إرسال تذكير الوتر\n"
        "▫️ /test_nawm — إرسال أذكار النوم\n"
        "▫️ /test_prayer — إرسال جدول مواقيت الصلاة\n"
        "▫️ /test_friday — إرسال تذكيرات الجمعة\n"
        "▫️ /test_dua — إرسال دعاء اليوم المأثور"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)

async def cmd_set_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تعيين معرف القناة المستهدفة"""
    if not is_admin(update.effective_user.id):
        return
        
    if not context.args:
        await update.message.reply_text(
            "<b>يرجى إرسال معرف القناة مع الأمر، مثال:</b>\n"
            "<code>/setchannel @MyChannel</code>\n"
            "أو إذا كانت خاصة:\n"
            "<code>/setchannel -1001234567890</code>",
            parse_mode=ParseMode.HTML
        )
        return
        
    new_ch = context.args[0].strip()
    set_channel_id(new_ch)
    
    # تحديث رابط الدعوة تلقائياً إذا كان المعرف باسم مستخدم
    if new_ch.startswith("@"):
        set_channel_link(f"https://t.me/{new_ch[1:]}")
        
    await update.message.reply_text(
        f"✅ <b>تم ضبط القناة المستهدفة بنجاح إلى:</b> <code>{new_ch}</code>\n"
        f"تأكد من ترقية البوت مشرفاً (Admin) في القناة ومنحه صلاحية نشر الرسائل.",
        parse_mode=ParseMode.HTML
    )

async def cmd_set_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تعيين رابط القناة"""
    if not is_admin(update.effective_user.id):
        return
    if not context.args:
        await update.message.reply_text("يرجى كتابة الرابط مع الأمر، مثال: <code>/setlink https://t.me/example</code>", parse_mode=ParseMode.HTML)
        return
    link = context.args[0].strip()
    set_channel_link(link)
    await update.message.reply_text(f"✅ تم ضبط رابط القناة إلى: {link}")

async def cmd_set_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تعيين الصفحة الحالية من مصحف مجمع الملك فهد"""
    if not is_admin(update.effective_user.id):
        return
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("يرجى إدخال رقم الصفحة (من 1 إلى 604)، مثال: <code>/setpage 50</code>", parse_mode=ParseMode.HTML)
        return
    p = int(context.args[0])
    if p < 1 or p > 604:
        await update.message.reply_text("⚠️ يجب أن يكون رقم الصفحة بين 1 و 604.")
        return
    actual = set_current_page(p)
    await update.message.reply_text(f"✅ تم ضبط صفحة الورد القادم على الصفحة رقم: <b>{actual}</b> بمصحف المدينة النبوية.", parse_mode=ParseMode.HTML)

async def cmd_set_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تعيين عدد صفحات القرآن اليومية"""
    if not is_admin(update.effective_user.id):
        return
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("يرجى إدخال عدد الصفحات (مثال: <code>/setrate 2</code>)", parse_mode=ParseMode.HTML)
        return
    rate = int(context.args[0])
    set_quran_pages_per_day(rate)
    await update.message.reply_text(f"✅ تم ضبط معدل القراءة اليومي على <b>{rate}</b> صفحة يومياً.", parse_mode=ParseMode.HTML)

async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض تقرير شامل عن حالة البوت"""
    if not is_admin(update.effective_user.id):
        return
    
    ch = get_channel_id() or "غير محددة"
    st = load_state()
    pt = await get_makkah_prayer_times()
    timings = pt.get("timings", {})
    
    report = (
        "<b>📊 تقرير حالة بوت الأذكار والقرآن الكريم:</b>\n\n"
        f"📢 <b>القناة:</b> <code>{ch}</code>\n"
        f"📖 <b>مصحف المدينة (مجمع الملك فهد):</b> صفحة {st.get('current_page', 1)} / 604\n"
        f"🏅 <b>الختمات:</b> {st.get('khatmah_count', 0)}\n"
        f"📅 <b>تاريخ آخر إرسال:</b> {st.get('last_sent_date', 'لم يبدأ بعد')}\n\n"
        "<b>🕋 مواقيت مكة المكرمة اليوم (تقويم أم القرى):</b>\n"
        f"▫️ الفجر: {timings.get('Fajr')} | الظهر: {timings.get('Dhuhr')}\n"
        f"▫️ العصر: {timings.get('Asr')} | المغرب: {timings.get('Maghrib')}\n"
        f"▫️ العشاء: {timings.get('Isha')} | الوتر: {timings.get('Lastthird')}\n\n"
        "✅ <b>الجدولة التلقائية نشطة وتعمل على مدار 24 ساعة.</b>"
    )
    await update.message.reply_text(report, parse_mode=ParseMode.HTML)

# أوامر الاختبار الفوري في القناة
async def cmd_test_quran(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    await update.message.reply_text("⏳ جاري تجهيز وإرسال ورد القرآن لمصحف مجمع الملك فهد إلى القناة...")
    pages = await get_daily_wird_pages()
    ok = await send_channel_quran_pages(context.bot, pages)
    if ok:
        advance_wird_state(len(pages))
        await update.message.reply_text("✅ تم إرسال ورد القرآن الكريم بنجاح إلى القناة!")
    else:
        await update.message.reply_text("❌ تعذر الإرسال للقناة. تأكد من ضبط /setchannel وأن البوت مشرف في القناة.")

async def cmd_test_sabah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    msg = format_adhkar_sabah_post(ADHKAR_SABAH)
    ok = await send_channel_message(context.bot, msg)
    await update.message.reply_text("✅ تم إرسال أذكار الصباح للقناة." if ok else "❌ فشل الإرسال للقناة.")

async def cmd_test_masa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    msg = format_adhkar_masa_post(ADHKAR_MASA)
    ok = await send_channel_message(context.bot, msg)
    await update.message.reply_text("✅ تم إرسال أذكار المساء للقناة." if ok else "❌ فشل الإرسال للقناة.")

async def cmd_test_witr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    import random
    item = random.choice(WITR_REMINDERS)
    msg = format_witr_reminder(item)
    ok = await send_channel_message(context.bot, msg)
    await update.message.reply_text("✅ تم إرسال تذكير الوتر للقناة." if ok else "❌ فشل الإرسال للقناة.")

async def cmd_test_nawm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    msg = format_adhkar_nawm_post(ADHKAR_NAWM)
    ok = await send_channel_message(context.bot, msg)
    await update.message.reply_text("✅ تم إرسال أذكار النوم للقناة." if ok else "❌ فشل الإرسال للقناة.")

async def cmd_test_prayer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    pt = await get_makkah_prayer_times()
    msg = format_prayer_table_post(pt["hijri"], pt["gregorian"], pt["timings"])
    ok = await send_channel_message(context.bot, msg)
    await update.message.reply_text("✅ تم إرسال جدول مواقيت الصلاة للقناة." if ok else "❌ فشل الإرسال للقناة.")

async def cmd_test_friday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    msg = format_friday_kahf_post(FRIDAY_REMINDERS["kahf"])
    ok = await send_channel_message(context.bot, msg)
    await update.message.reply_text("✅ تم إرسال تذكير الجمعة للقناة." if ok else "❌ فشل الإرسال للقناة.")

async def cmd_test_dua(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    import random
    item = random.choice(AUTHENTIC_DUAS)
    msg = format_daily_dua_post(item)
    ok = await send_channel_message(context.bot, msg)
    await update.message.reply_text("✅ تم إرسال دعاء اليوم المأثور للقناة." if ok else "❌ فشل الإرسال للقناة.")
