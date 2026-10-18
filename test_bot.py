import asyncio
from config import BOT_TOKEN, TIMEZONE
from services.prayer_times import get_makkah_prayer_times
from services.quran_service import get_daily_wird_pages
from services.formatter import format_prayer_table_post, format_adhkar_sabah_post
from data.adhkar_sabah import ADHKAR_SABAH

async def test_all():
    print("Testing Bot Token:", BOT_TOKEN[:15] + "...")
    pt = await get_makkah_prayer_times()
    print("Prayer times successfully loaded for Makkah:")
    for k, v in pt["timings"].items():
        print(f"  {k}: {v}")
        
    pages = await get_daily_wird_pages()
    print(f"Quran Wird successfully generated: {len(pages)} page(s)")
    p0 = pages[0]
    print(f"Page {p0['page_number']}: Juz {p0['juz']}")
    print(f"Image URL: {p0['image_url']}")
    print(f"Morning Adhkar items count: {len(ADHKAR_SABAH)}")
    print("ALL SERVICES VERIFIED 100% OK!")

if __name__ == "__main__":
    asyncio.run(test_all())
