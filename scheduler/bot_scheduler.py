"""
محرك الجدولة الآلية لبوت الأذكار والقرآن الكريم
يعمل على مدار 24 ساعة متزامناً بدقة مع توقيت مكة المكرمة (Asia/Riyadh)
"""
import random
import logging
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from telegram import Bot

from config import TIMEZONE
from services.prayer_times import get_makkah_prayer_times, ARABIC_PRAYER_NAMES
from services.quran_service import get_daily_wird_pages, advance_wird_state
from services.formatter import (
    format_prayer_table_post,
    format_adhkar_sabah_post,
    format_adhkar_masa_post,
    format_adhkar_nawm_post,
    format_witr_reminder,
    format_azan_reminder,
    format_duha_reminder,
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
MAKKAH_TZ = pytz.timezone(TIMEZONE)

scheduler = AsyncIOScheduler(timezone=MAKKAH_TZ)
_bot_instance: Bot = None

# وظائف النشر المجدولة

async def job_daily_prayer_table():
    """نشر بطاقة مواقيت الصلاة في مطلع اليوم وإعادة ضبط منبهات الأذان"""
    logger.info("Running job_daily_prayer_table...")
    pt = await get_makkah_prayer_times()
    timings = pt.get("timings", {})
    msg = format_prayer_table_post(pt["hijri"], pt["gregorian"], timings)
    await send_channel_message(_bot_instance, msg)
    
    # تحديث مواعيد الأذان الديناميكية لليوم
    schedule_today_azan_jobs(timings)

async def job_morning_adhkar():
    """نشر أذكار الصباح المباركة"""
    logger.info("Running job_morning_adhkar...")
    msg = format_adhkar_sabah_post(ADHKAR_SABAH)
    await send_channel_message(_bot_instance, msg)

async def job_quran_wird():
    """نشر ورد القرآن الكريم اليومي (مصحف مجمع الملك فهد)"""
    logger.info("Running job_quran_wird...")
    pages = await get_daily_wird_pages()
    ok = await send_channel_quran_pages(_bot_instance, pages)
    if ok:
        advance_wird_state(len(pages))

async def job_duha_reminder():
    """تذكير صلاة الضحى"""
    logger.info("Running job_duha_reminder...")
    msg = format_duha_reminder()
    await send_channel_message(_bot_instance, msg)

async def job_evening_adhkar():
    """نشر أذكار المساء المباركة"""
    logger.info("Running job_evening_adhkar...")
    msg = format_adhkar_masa_post(ADHKAR_MASA)
    await send_channel_message(_bot_instance, msg)

async def job_sleep_adhkar():
    """نشر أذكار النوم الصحيحة"""
    logger.info("Running job_sleep_adhkar...")
    msg = format_adhkar_nawm_post(ADHKAR_NAWM)
    await send_channel_message(_bot_instance, msg)

async def job_witr_reminder():
    """تذكير صلاة الوتر وقيام الليل في ثلث الليل الأخير"""
    logger.info("Running job_witr_reminder...")
    item = random.choice(WITR_REMINDERS)
    msg = format_witr_reminder(item)
    await send_channel_message(_bot_instance, msg)

async def job_daily_dua():
    """نشر دعاء اليوم المأثور"""
    logger.info("Running job_daily_dua...")
    item = random.choice(AUTHENTIC_DUAS)
    msg = format_daily_dua_post(item)
    await send_channel_message(_bot_instance, msg)

async def job_friday_kahf():
    """تذكير سورة الكهف صباح الجمعة"""
    logger.info("Running job_friday_kahf...")
    msg = format_friday_kahf_post(FRIDAY_REMINDERS["kahf"])
    await send_channel_message(_bot_instance, msg)

async def job_friday_salawat():
    """تذكير الصلاة على النبي ﷺ يوم الجمعة"""
    logger.info("Running job_friday_salawat...")
    msg = format_friday_salawat_post(FRIDAY_REMINDERS["salawat"])
    await send_channel_message(_bot_instance, msg)

async def job_friday_istijaba():
    """تذكير ساعة الإجابة عصر الجمعة"""
    logger.info("Running job_friday_istijaba...")
    msg = format_friday_istijaba_post(FRIDAY_REMINDERS["saat_istijaba"])
    await send_channel_message(_bot_instance, msg)

async def trigger_azan(prayer_name_ar: str, prayer_time_str: str):
    """إرسال تنبيه الأذان في موعده المحدد"""
    logger.info(f"Triggering azan alert for {prayer_name_ar} at {prayer_time_str} Makkah time.")
    msg = format_azan_reminder(prayer_name_ar, prayer_time_str)
    await send_channel_message(_bot_instance, msg)

def schedule_today_azan_jobs(timings: dict):
    """جدولة تنبيهات الأذان الخمسة لليوم حسب مواقيت مكة المعتمدة"""
    now = datetime.now(MAKKAH_TZ)
    
    # قائمة الصلوات الأساسية للتنبيه
    for p_key in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]:
        time_str = timings.get(p_key)
        if not time_str:
            continue
            
        try:
            parts = time_str.split(":")
            hour = int(parts[0])
            minute = int(parts[1])
            
            p_datetime = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # إذا لم يمضِ الوقت بعد، نجدوله لليوم
            if p_datetime > now:
                job_id = f"azan_{p_key}_{now.strftime('%Y%m%d')}"
                # إزالة أي مهمة سابقة بنفس الاسم إن وجدت
                if scheduler.get_job(job_id):
                    scheduler.remove_job(job_id)
                    
                scheduler.add_job(
                    trigger_azan,
                    trigger=DateTrigger(run_date=p_datetime, timezone=MAKKAH_TZ),
                    args=[ARABIC_PRAYER_NAMES[p_key], time_str],
                    id=job_id,
                    replace_existing=True
                )
                logger.info(f"Scheduled Azan {p_key} for {time_str} today.")
        except Exception as e:
            logger.error(f"Error scheduling azan for {p_key}: {e}")

    # جدولة صلاة الضحى (20 دقيقة بعد الشروق)
    sunrise_str = timings.get("Sunrise")
    if sunrise_str:
        try:
            parts = sunrise_str.split(":")
            sunrise_dt = now.replace(hour=int(parts[0]), minute=int(parts[1]), second=0, microsecond=0)
            duha_dt = sunrise_dt + timedelta(minutes=20)
            if duha_dt > now:
                job_id = f"duha_{now.strftime('%Y%m%d')}"
                scheduler.add_job(
                    job_duha_reminder,
                    trigger=DateTrigger(run_date=duha_dt, timezone=MAKKAH_TZ),
                    id=job_id,
                    replace_existing=True
                )
        except Exception as e:
            logger.error(f"Error scheduling duha: {e}")

async def init_scheduler(bot: Bot):
    """بدء تشغيل الجدولة التلقائية وتثبيت المهام الثابتة"""
    global _bot_instance
    _bot_instance = bot
    
    # 1. نشر جدول مواقيت الصلاة في مطلع كل يوم (الساعة 00:05 ليلاً بتوقيت مكة)
    scheduler.add_job(
        job_daily_prayer_table,
        trigger=CronTrigger(hour=0, minute=5, timezone=MAKKAH_TZ),
        id="daily_prayer_table",
        replace_existing=True
    )
    
    # 2. أذكار الصباح (الساعة 06:15 صباحاً بتوقيت مكة)
    scheduler.add_job(
        job_morning_adhkar,
        trigger=CronTrigger(hour=6, minute=15, timezone=MAKKAH_TZ),
        id="morning_adhkar",
        replace_existing=True
    )
    
    # 3. ورد القرآن الكريم اليومي - مصحف مجمع الملك فهد (الساعة 08:00 صباحاً بتوقيت مكة)
    scheduler.add_job(
        job_quran_wird,
        trigger=CronTrigger(hour=8, minute=0, timezone=MAKKAH_TZ),
        id="quran_wird",
        replace_existing=True
    )
    
    # 4. دعاء اليوم المأثور (الساعة 13:30 بعد الظهر بتوقيت مكة)
    scheduler.add_job(
        job_daily_dua,
        trigger=CronTrigger(hour=13, minute=30, timezone=MAKKAH_TZ),
        id="daily_dua",
        replace_existing=True
    )
    
    # 5. أذكار المساء (الساعة 16:15 بعد العصر بتوقيت مكة)
    scheduler.add_job(
        job_evening_adhkar,
        trigger=CronTrigger(hour=16, minute=15, timezone=MAKKAH_TZ),
        id="evening_adhkar",
        replace_existing=True
    )
    
    # 6. أذكار النوم الصحيحة (الساعة 22:30 ليلاً بتوقيت مكة)
    scheduler.add_job(
        job_sleep_adhkar,
        trigger=CronTrigger(hour=22, minute=30, timezone=MAKKAH_TZ),
        id="sleep_adhkar",
        replace_existing=True
    )
    
    # 7. تذكير صلاة الوتر وقيام الليل (الساعة 01:45 في ثلث الليل الأخير بتوقيت مكة)
    scheduler.add_job(
        job_witr_reminder,
        trigger=CronTrigger(hour=1, minute=45, timezone=MAKKAH_TZ),
        id="witr_reminder",
        replace_existing=True
    )
    
    # 8. سنن يوم الجمعة المبارك
    # تذكير سورة الكهف صباح الجمعة (08:30 صباحاً)
    scheduler.add_job(
        job_friday_kahf,
        trigger=CronTrigger(day_of_week="fri", hour=8, minute=30, timezone=MAKKAH_TZ),
        id="friday_kahf",
        replace_existing=True
    )
    # الإكثار من الصلاة على النبي ﷺ (11:30 صباح الجمعة)
    scheduler.add_job(
        job_friday_salawat,
        trigger=CronTrigger(day_of_week="fri", hour=11, minute=30, timezone=MAKKAH_TZ),
        id="friday_salawat",
        replace_existing=True
    )
    # ساعة الإجابة قبل غروب شمس الجمعة (16:45 مساء الجمعة)
    scheduler.add_job(
        job_friday_istijaba,
        trigger=CronTrigger(day_of_week="fri", hour=16, minute=45, timezone=MAKKAH_TZ),
        id="friday_istijaba",
        replace_existing=True
    )
    
    # جلب مواقيت اليوم وجدولة مواعيد الأذان الحالية فور التشغيل
    try:
        pt = await get_makkah_prayer_times()
        schedule_today_azan_jobs(pt.get("timings", {}))
    except Exception as e:
        logger.error(f"Error initializing today's prayer timings: {e}")
        
    scheduler.start()
    logger.info("Makkah Islamic Bot Scheduler started successfully.")
