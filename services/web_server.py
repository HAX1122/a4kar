"""
خادم الويب الخفيف للفحص السحابي (Keep-Alive Health Server)
مهم لضمان استمرار عمل البوت على المنصات السحابية (Render, Railway, Fly.io, Koyeb) طوال 24 ساعة
"""
import time
import logging
from aiohttp import web
from datetime import datetime
import pytz

from config import PORT, get_channel_id, TIMEZONE
from services.quran_service import load_state

logger = logging.getLogger(__name__)
START_TIME = time.time()
MAKKAH_TZ = pytz.timezone(TIMEZONE)

async def health_handler(request):
    """Endpoint for uptime monitors and container health checks."""
    now_makkah = datetime.now(MAKKAH_TZ).strftime("%Y-%m-%d %H:%M:%S")
    uptime = int(time.time() - START_TIME)
    state = load_state()
    
    return web.json_response({
        "status": "healthy",
        "service": "Makkah Islamic Bot 24/7",
        "makkah_time": now_makkah,
        "uptime_seconds": uptime,
        "target_channel": get_channel_id() or "Not set yet",
        "quran_current_page": state.get("current_page", 1),
        "khatmah_count": state.get("khatmah_count", 0)
    })

async def root_handler(request):
    """Simple friendly page."""
    now_makkah = datetime.now(MAKKAH_TZ).strftime("%Y-%m-%d %H:%M:%S")
    html_content = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
        <meta charset="utf-8">
        <title>بوت الأذكار والقرآن الكريم - مكة المكرمة</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; text-align: center; padding: 50px; }}
            .card {{ background: #1e293b; max-width: 600px; margin: 0 auto; padding: 30px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.4); border: 1px solid #334155; }}
            h1 {{ color: #38bdf8; }}
            .badge {{ display: inline-block; padding: 6px 16px; background: #10b981; color: white; border-radius: 20px; font-weight: bold; margin-bottom: 20px; }}
            .meta {{ text-align: right; margin-top: 25px; line-height: 1.8; color: #cbd5e1; }}
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">يعمل سحابياً 24/7 بنجاح</span>
            <h1>🕋 بوت الأذكار والقرآن الكريم</h1>
            <p>خادم البوت السحابي متصل ويعمل وفق توقيت مكة المكرمة وتقويم أم القرى.</p>
            <div class="meta">
                <p>📍 <b>الوقت الحالي في مكة:</b> {now_makkah}</p>
                <p>📖 <b>الصفحة الحالية من المصحف الشريف:</b> {load_state().get('current_page', 1)}</p>
                <p>📢 <b>القناة المستهدفة:</b> {get_channel_id() or 'يرجى ضبطها عبر الأمر /setchannel'}</p>
            </div>
        </div>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type="text/html")

async def start_web_server():
    """Start the aiohttp background web runner."""
    app = web.Application()
    app.router.add_get("/", root_handler)
    app.router.add_get("/health", health_handler)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"Keep-Alive Health Server started on port {PORT}")
