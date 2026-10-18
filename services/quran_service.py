"""
خدمة ورد القرآن الكريم اليومي
مصحف مجمع الملك فهد لطباعة المصحف الشريف بالمدينة المنورة (رواية حفص عن عاصم - 604 صفحة)
"""
import json
import logging
from pathlib import Path
from datetime import datetime
import pytz
import httpx

from config import get_quran_pages_per_day
from data.quran_metadata import (
    get_juz_for_page,
    get_surahs_for_page,
    get_page_image_urls,
    get_audio_recitation_url
)
from services.formatter import format_quran_wird_caption

logger = logging.getLogger(__name__)

STATE_FILE = Path(__file__).resolve().parent.parent / "data" / "state.json"
MAKKAH_TZ = pytz.timezone("Asia/Riyadh")

def load_state() -> dict:
    """تحميل حالة تقدم القراءة وختمات القرآن"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading state.json: {e}")
    # الحالة الافتراضية: البدء من الصفحة الأولى
    return {
        "current_page": 1,
        "khatmah_count": 0,
        "total_pages_sent": 0,
        "last_sent_date": None
    }

def save_state(state: dict):
    """حفظ حالة القراءة والصفحة الحالية"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def set_current_page(page_num: int):
    """تعديل رقم الصفحة الحالية يدوياً بواسطة الأدمن"""
    st = load_state()
    st["current_page"] = max(1, min(604, page_num))
    save_state(st)
    return st["current_page"]

async def fetch_page_tafsir_snippet(page: int) -> str:
    """
    جلب قبس من التفسير الميسر المعتمد من مجمع الملك فهد لآيات الصفحة
    """
    url = f"https://api.quran.com/api/v4/verses/by_page/{page}?words=false&tafsirs=16"
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                verses = data.get("verses", [])
                if verses:
                    # نأخذ تفسير أول آية في الصفحة كقبس تدبري
                    first_verse = verses[0]
                    tafsir_text = first_verse.get("tafsir", {}).get("text", "")
                    if not tafsir_text:
                        # جلب مباشر للتفسير الميسر للآية
                        vk = first_verse.get("verse_key")
                        if vk:
                            t_url = f"https://api.quran.com/api/v4/quran/tafsirs/16?verse_key={vk}"
                            t_resp = await client.get(t_url)
                            if t_resp.status_code == 200:
                                t_data = t_resp.json()
                                tafsirs = t_data.get("tafsirs", [])
                                if tafsirs:
                                    raw = tafsirs[0].get("text", "")
                                    # إزالة أي وسوم html بسيطة
                                    clean = raw.replace("<p>", "").replace("</p>", "").strip()
                                    return clean[:300] + ("..." if len(clean) > 300 else "")
    except Exception as e:
        logger.warning(f"Could not fetch live tafsir for page {page}: {e}")
    
    return "تدبر آيات الله واستشعر خطابه لك؛ فإن القرآن مأدبة الله ونوره المبين."

async def get_daily_wird_pages() -> list[dict]:
    """
    تجهيز صفحات الورد اليومي مع الصور والكابشن المعتمد لمجمع الملك فهد
    """
    state = load_state()
    start_page = state.get("current_page", 1)
    pages_count = get_quran_pages_per_day()
    
    pages_to_send = []
    current = start_page
    
    for _ in range(pages_count):
        if current > 604:
            current = 1
            state["khatmah_count"] = state.get("khatmah_count", 0) + 1
            
        juz = get_juz_for_page(current)
        surahs = get_surahs_for_page(current)
        surah_names = " و ".join([s["name"] for s in surahs])
        
        # جلب روابط صور الصفحة من خوادم مصحف المدينة
        image_urls = get_page_image_urls(current)
        
        # قبس من التفسير الميسر
        tafsir = await fetch_page_tafsir_snippet(current)
        
        caption = format_quran_wird_caption(
            page=current,
            surah_name=surah_names,
            juz=juz,
            tafsir_snippet=tafsir
        )
        
        pages_to_send.append({
            "page_number": current,
            "juz": juz,
            "surah_name": surah_names,
            "image_url": image_urls[0],
            "fallback_image_url": image_urls[1],
            "caption": caption
        })
        
        current += 1

    return pages_to_send

def advance_wird_state(pages_sent_count: int):
    """تحديث مؤشر الصفحة بعد الإرسال بنجاح"""
    state = load_state()
    current = state.get("current_page", 1)
    new_page = current + pages_sent_count
    
    if new_page > 604:
        new_page = (new_page - 604)
        state["khatmah_count"] = state.get("khatmah_count", 0) + 1
        
    state["current_page"] = new_page
    state["total_pages_sent"] = state.get("total_pages_sent", 0) + pages_sent_count
    state["last_sent_date"] = datetime.now(MAKKAH_TZ).strftime("%Y-%m-%d")
    save_state(state)
    logger.info(f"Advanced Quran state to page {new_page}.")
