"""
Configuration module for Makkah Islamic Bot
إعدادات بوت الأذكار والقرآن الكريم - توقيت مكة المكرمة
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

CONFIG_FILE = BASE_DIR / "data" / "settings.json"

def load_settings():
    """Load dynamic settings saved by admin commands."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_settings(settings: dict):
    """Save dynamic settings."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

_settings = load_settings()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "8884360148:AAEsmY-AZEYDMdE72BLcmm6zmjrK_p64U4c").strip()

# Target Channel ID (e.g. "@my_channel" or "-1001234567890")
def get_channel_id() -> str:
    current = load_settings().get("channel_id")
    if current:
        return str(current)
    return os.getenv("CHANNEL_ID", "").strip()

def set_channel_id(new_id: str):
    s = load_settings()
    s["channel_id"] = new_id.strip()
    save_settings(s)

# Admin Telegram User IDs (for private management)
def get_admin_ids() -> list[int]:
    admins_str = os.getenv("ADMIN_IDS", "")
    admins = []
    for item in admins_str.split(","):
        item = item.strip()
        if item.isdigit():
            admins.append(int(item))
    # Also load from dynamic settings
    saved = load_settings().get("admin_ids", [])
    for a in saved:
        if a not in admins:
            admins.append(a)
    return admins

def add_admin_id(user_id: int):
    s = load_settings()
    current = s.get("admin_ids", [])
    if user_id not in current:
        current.append(user_id)
        s["admin_ids"] = current
        save_settings(s)

# Timezone: Asia/Riyadh (توقيت مكة المكرمة)
TIMEZONE = os.getenv("TIMEZONE", "Asia/Riyadh")

# Number of Quran pages sent per day (افتراضياً صفحتين يومياً أو صفحة واحدة)
def get_quran_pages_per_day() -> int:
    return int(load_settings().get("quran_pages_per_day", os.getenv("QURAN_PAGES_PER_DAY", "2")))

def set_quran_pages_per_day(count: int):
    s = load_settings()
    s["quran_pages_per_day"] = max(1, min(20, count))
    save_settings(s)

# Channel Invite Link (for private redirect message)
def get_channel_link() -> str:
    s = load_settings()
    return s.get("channel_link", os.getenv("CHANNEL_LINK", "https://t.me/"))

def set_channel_link(link: str):
    s = load_settings()
    s["channel_link"] = link.strip()
    save_settings(s)

# Port for Keep-Alive Web Server (for cloud hosting like Render/Railway/Fly.io)
PORT = int(os.getenv("PORT", "8080"))

# Umm Al-Qura Calculation Method ID (جامعة أم القرى - مكة المكرمة)
PRAYER_METHOD = 4
MAKKAH_LAT = 21.4225
MAKKAH_LON = 39.8262
