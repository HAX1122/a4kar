"""
وحدة إرسال المنشورات إلى القناة الرسمية
تتولى إدارة إرسال الرسائل والصور والألبومات مع معالجة الأخطاء والتأكد من الصلاحيات
"""
import logging
from telegram import Bot, InputMediaPhoto
from telegram.constants import ParseMode
from telegram.error import TelegramError

from config import get_channel_id

logger = logging.getLogger(__name__)

async def send_channel_message(bot: Bot, text: str) -> bool:
    """إرسال رسالة نصية منسقة بـ HTML إلى القناة الرسمية"""
    channel_id = get_channel_id()
    if not channel_id:
        logger.warning("No channel ID configured. Please set CHANNEL_ID via .env or /setchannel.")
        return False
        
    try:
        await bot.send_message(
            chat_id=channel_id,
            text=text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False
        )
        logger.info(f"Message successfully sent to channel {channel_id}.")
        return True
    except TelegramError as e:
        logger.error(f"Telegram error sending to channel {channel_id}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending message: {e}")
        return False

async def send_channel_photo(bot: Bot, photo_url: str, caption: str, fallback_url: str = "") -> bool:
    """إرسال صورة واحدة مع كابشن منسق إلى القناة"""
    channel_id = get_channel_id()
    if not channel_id:
        logger.warning("No channel ID configured.")
        return False
        
    # محاولة الرابط الأساسي
    try:
        await bot.send_photo(
            chat_id=channel_id,
            photo=photo_url,
            caption=caption,
            parse_mode=ParseMode.HTML
        )
        logger.info(f"Photo successfully sent to channel {channel_id}.")
        return True
    except Exception as e:
        logger.warning(f"Failed to send primary photo URL ({photo_url}): {e}")
        if fallback_url:
            try:
                await bot.send_photo(
                    chat_id=channel_id,
                    photo=fallback_url,
                    caption=caption,
                    parse_mode=ParseMode.HTML
                )
                logger.info("Photo sent successfully using fallback URL.")
                return True
            except Exception as e2:
                logger.error(f"Failed fallback photo too: {e2}")
        
        # في حال تعذر تحميل الصورة يتم إرسال النص لتفادي فوات الورد
        await send_channel_message(bot, caption)
        return False

async def send_channel_quran_pages(bot: Bot, pages: list[dict]) -> bool:
    """
    إرسال صفحات ورد القرآن الكريم
    إذا كانت صفحتين فأكثر يتم إرسالها كألبوم (Media Group) لعرضها متجاورة كالمصحف المفتوح
    """
    channel_id = get_channel_id()
    if not channel_id:
        logger.warning("No channel ID configured.")
        return False

    if not pages:
        return False

    if len(pages) == 1:
        p = pages[0]
        return await send_channel_photo(
            bot=bot,
            photo_url=p["image_url"],
            caption=p["caption"],
            fallback_url=p.get("fallback_image_url", "")
        )
    
    # إرسال صفحتين كألبوم متجاور
    media = []
    for idx, p in enumerate(pages):
        # الكابشن يوضع على الصفحة الأولى فقط في الألبوم
        caption = p["caption"] if idx == 0 else ""
        media.append(
            InputMediaPhoto(
                media=p["image_url"],
                caption=caption,
                parse_mode=ParseMode.HTML
            )
        )
    
    try:
        await bot.send_media_group(chat_id=channel_id, media=media)
        logger.info(f"Sent {len(pages)} Quran pages as media album to channel {channel_id}.")
        return True
    except Exception as e:
        logger.warning(f"Media group failed ({e}), falling back to sending page by page...")
        success = True
        for p in pages:
            ok = await send_channel_photo(
                bot,
                p["image_url"],
                p["caption"],
                p.get("fallback_image_url", "")
            )
            if not ok:
                success = False
        return success
