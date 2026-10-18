"""
خدمة مواقيت الصلاة في مكة المكرمة
وفق تقويم أم القرى الرسمي (Method 4: Umm Al-Qura University, Makkah)
"""
import logging
import httpx
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)

MAKKAH_TZ = pytz.timezone("Asia/Riyadh")

ARABIC_PRAYER_NAMES = {
    "Fajr": "الفجر",
    "Sunrise": "الشروق",
    "Dhuhr": "الظهر",
    "Asr": "العصر",
    "Maghrib": "المغرب",
    "Isha": "العشاء"
}

# Fallback approximate times for Makkah in case of complete internet outage
FALLBACK_TIMINGS = {
    "Fajr": "05:00",
    "Sunrise": "06:18",
    "Dhuhr": "12:08",
    "Asr": "15:28",
    "Maghrib": "17:55",
    "Isha": "19:25",
    "Lastthird": "02:10"
}

_cache = {
    "date": None,
    "timings": None,
    "hijri": None,
    "gregorian": None
}

async def get_makkah_prayer_times() -> dict:
    """
    استرجاع مواقيت الصلاة لمكة المكرمة بتقويم أم القرى الرسمي
    """
    now = datetime.now(MAKKAH_TZ)
    date_str = now.strftime("%d-%m-%Y")
    
    # Return from cache if already retrieved for today
    if _cache["date"] == date_str and _cache["timings"]:
        return _cache
    
    url = f"https://api.aladhan.com/v1/timingsByCity/{date_str}?city=Makkah&country=Saudi+Arabia&method=4"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                data_inner = data.get("data", {})
                raw_timings = data_inner.get("timings", {})
                
                # Clean up timings (remove any '(+03)' suffix if present)
                clean_timings = {}
                for k, v in raw_timings.items():
                    clean_timings[k] = v.split(" ")[0].strip()
                
                hijri_info = data_inner.get("date", {}).get("hijri", {})
                hijri_day = hijri_info.get("day", "")
                hijri_month = hijri_info.get("month", {}).get("ar", "")
                hijri_year = hijri_info.get("year", "")
                hijri_formatted = f"{hijri_day} {hijri_month} {hijri_year} هـ"
                
                greg_info = data_inner.get("date", {}).get("gregorian", {})
                greg_formatted = f"{greg_info.get('day', '')} {greg_info.get('month', {}).get('en', '')} {greg_info.get('year', '')}"
                
                _cache["date"] = date_str
                _cache["timings"] = clean_timings
                _cache["hijri"] = hijri_formatted
                _cache["gregorian"] = greg_formatted
                
                logger.info(f"Retrieved Makkah prayer times for {date_str} successfully.")
                return _cache
            else:
                logger.warning(f"AlAdhan API returned status {resp.status_code}, using fallback.")
    except Exception as e:
        logger.error(f"Error fetching Makkah prayer times from API: {e}. Using fallback.")
    
    # Fallback
    _cache["date"] = date_str
    _cache["timings"] = FALLBACK_TIMINGS
    _cache["hijri"] = "مكة المكرمة"
    _cache["gregorian"] = now.strftime("%d/%m/%Y")
    return _cache

def parse_time_for_today(time_str: str) -> datetime:
    """Parse 'HH:MM' string to datetime localized to Makkah timezone for today."""
    now = datetime.now(MAKKAH_TZ)
    parts = time_str.split(":")
    hour = int(parts[0])
    minute = int(parts[1])
    return MAKKAH_TZ.localize(datetime(now.year, now.month, now.day, hour, minute, 0))
