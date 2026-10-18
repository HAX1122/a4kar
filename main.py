"""
الملف الرئيسي لتشغيل بوت الأذكار والقرآن الكريم ومواقيت مكة المكرمة 24/7
Makkah Islamic Bot Entry Point
"""
import asyncio
import logging
import sys
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    Application
)

from config import BOT_TOKEN
from bot.handlers import (
    cmd_start,
    cmd_set_channel,
    cmd_set_link,
    cmd_set_page,
    cmd_set_rate,
    cmd_status,
    cmd_test_quran,
    cmd_test_sabah,
    cmd_test_masa,
    cmd_test_witr,
    cmd_test_nawm,
    cmd_test_prayer,
    cmd_test_friday,
    cmd_test_dua,
    handle_private_message
)
from scheduler.bot_scheduler import init_scheduler
from services.web_server import start_web_server

# إعداد التسجيل (Logging)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("MakkahIslamicBot")

async def post_init(application: Application):
    """تهيئة الخوادم الخلفية والجدولة بعد اتصال البوت بالتيليجرام"""
    bot = application.bot
    bot_info = await bot.get_me()
    logger.info(f"Bot connected successfully as: @{bot_info.username} ({bot_info.first_name})")
    
    # 1. تشغيل خادم الفحص السحابي (Keep-Alive Web Server)
    try:
        await start_web_server()
    except Exception as e:
        logger.error(f"Failed to start keepalive web server: {e}")
        
    # 2. تشغيل محرك الجدولة التلقائية
    try:
        await init_scheduler(bot)
    except Exception as e:
        logger.error(f"Failed to initialize scheduler: {e}")

def main():
    """نقطة الدخول الرئيسية"""
    if not BOT_TOKEN or "YOUR_BOT_TOKEN" in BOT_TOKEN:
        logger.critical("Error: BOT_TOKEN is not configured! Please set it in .env")
        sys.exit(1)
        
    logger.info("Initializing Makkah Islamic Bot...")
    
    # بناء تطبيق التيليجرام
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )
    
    # تسجيل أوامر الأدمن
    application.add_handler(CommandHandler("start", cmd_start))
    application.add_handler(CommandHandler("setchannel", cmd_set_channel))
    application.add_handler(CommandHandler("setlink", cmd_set_link))
    application.add_handler(CommandHandler("setpage", cmd_set_page))
    application.add_handler(CommandHandler("setrate", cmd_set_rate))
    application.add_handler(CommandHandler("status", cmd_status))
    
    # أوامر الاختبار الفوري
    application.add_handler(CommandHandler("test_quran", cmd_test_quran))
    application.add_handler(CommandHandler("test_sabah", cmd_test_sabah))
    application.add_handler(CommandHandler("test_masa", cmd_test_masa))
    application.add_handler(CommandHandler("test_witr", cmd_test_witr))
    application.add_handler(CommandHandler("test_nawm", cmd_test_nawm))
    application.add_handler(CommandHandler("test_prayer", cmd_test_prayer))
    application.add_handler(CommandHandler("test_friday", cmd_test_friday))
    application.add_handler(CommandHandler("test_dua", cmd_test_dua))
    
    # معالجة أي رسائل أخرى في الخاص لمنع التفاعل العشوائي وتوجيه الزوار للقناة
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND, handle_private_message))
    
    logger.info("Starting polling loop...")
    # drop_pending_updates يتجاهل الرسائل القديمة المتراكمة أثناء توقف البوت
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
