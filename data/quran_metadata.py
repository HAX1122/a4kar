"""
بيانات المصحف الشريف - مجمع الملك فهد لطباعة المصحف الشريف بالمدينة المنورة
رواية حفص عن عاصم (مصحف المدينة النبوية - 604 صفحة)
"""

SURAH_LIST = [
    {"id": 1, "name": "الفاتحة", "type": "مكية", "verses": 7, "start_page": 1},
    {"id": 2, "name": "البقرة", "type": "مدنية", "verses": 286, "start_page": 2},
    {"id": 3, "name": "آل عمران", "type": "مدنية", "verses": 200, "start_page": 50},
    {"id": 4, "name": "النساء", "type": "مدنية", "verses": 176, "start_page": 77},
    {"id": 5, "name": "المائدة", "type": "مدنية", "verses": 120, "start_page": 106},
    {"id": 6, "name": "الأنعام", "type": "مكية", "verses": 165, "start_page": 128},
    {"id": 7, "name": "الأعراف", "type": "مكية", "verses": 206, "start_page": 151},
    {"id": 8, "name": "الأنفال", "type": "مدنية", "verses": 75, "start_page": 177},
    {"id": 9, "name": "التوبة", "type": "مدنية", "verses": 129, "start_page": 187},
    {"id": 10, "name": "يونس", "type": "مكية", "verses": 109, "start_page": 208},
    {"id": 11, "name": "هود", "type": "مكية", "verses": 123, "start_page": 221},
    {"id": 12, "name": "يوسف", "type": "مكية", "verses": 111, "start_page": 235},
    {"id": 13, "name": "الرعد", "type": "مدنية", "verses": 43, "start_page": 249},
    {"id": 14, "name": "إبراهيم", "type": "مكية", "verses": 52, "start_page": 255},
    {"id": 15, "name": "الحجر", "type": "مكية", "verses": 99, "start_page": 262},
    {"id": 16, "name": "النحل", "type": "مكية", "verses": 128, "start_page": 267},
    {"id": 17, "name": "الإسراء", "type": "مكية", "verses": 111, "start_page": 282},
    {"id": 18, "name": "الكهف", "type": "مكية", "verses": 110, "start_page": 293},
    {"id": 19, "name": "مريم", "type": "مكية", "verses": 98, "start_page": 305},
    {"id": 20, "name": "طه", "type": "مكية", "verses": 135, "start_page": 312},
    {"id": 21, "name": "الأنبياء", "type": "مكية", "verses": 112, "start_page": 322},
    {"id": 22, "name": "الحج", "type": "مدنية", "verses": 78, "start_page": 332},
    {"id": 23, "name": "المؤمنون", "type": "مكية", "verses": 118, "start_page": 342},
    {"id": 24, "name": "النور", "type": "مدنية", "verses": 64, "start_page": 350},
    {"id": 25, "name": "الفرقان", "type": "مكية", "verses": 77, "start_page": 359},
    {"id": 26, "name": "الشعراء", "type": "مكية", "verses": 227, "start_page": 367},
    {"id": 27, "name": "النمل", "type": "مكية", "verses": 93, "start_page": 377},
    {"id": 28, "name": "القصص", "type": "مكية", "verses": 88, "start_page": 385},
    {"id": 29, "name": "العنكبوت", "type": "مكية", "verses": 69, "start_page": 396},
    {"id": 30, "name": "الروم", "type": "مكية", "verses": 60, "start_page": 404},
    {"id": 31, "name": "لقمان", "type": "مكية", "verses": 34, "start_page": 411},
    {"id": 32, "name": "السجدة", "type": "مكية", "verses": 30, "start_page": 415},
    {"id": 33, "name": "الأحزاب", "type": "مدنية", "verses": 73, "start_page": 418},
    {"id": 34, "name": "سبأ", "type": "مكية", "verses": 54, "start_page": 428},
    {"id": 35, "name": "فاطر", "type": "مكية", "verses": 45, "start_page": 434},
    {"id": 36, "name": "يس", "type": "مكية", "verses": 83, "start_page": 440},
    {"id": 37, "name": "الصافات", "type": "مكية", "verses": 182, "start_page": 446},
    {"id": 38, "name": "ص", "type": "مكية", "verses": 88, "start_page": 453},
    {"id": 39, "name": "الزمر", "type": "مكية", "verses": 75, "start_page": 458},
    {"id": 40, "name": "غافر", "type": "مكية", "verses": 85, "start_page": 467},
    {"id": 41, "name": "فصلت", "type": "مكية", "verses": 54, "start_page": 477},
    {"id": 42, "name": "الشورى", "type": "مكية", "verses": 53, "start_page": 483},
    {"id": 43, "name": "الزخرف", "type": "مكية", "verses": 89, "start_page": 489},
    {"id": 44, "name": "الدخان", "type": "مكية", "verses": 59, "start_page": 496},
    {"id": 45, "name": "الجاثية", "type": "مكية", "verses": 37, "start_page": 499},
    {"id": 46, "name": "الأحقاف", "type": "مكية", "verses": 35, "start_page": 502},
    {"id": 47, "name": "محمد", "type": "مدنية", "verses": 38, "start_page": 507},
    {"id": 48, "name": "الفتح", "type": "مدنية", "verses": 29, "start_page": 511},
    {"id": 49, "name": "الحجرات", "type": "مدنية", "verses": 18, "start_page": 515},
    {"id": 50, "name": "ق", "type": "مكية", "verses": 45, "start_page": 518},
    {"id": 51, "name": "الذاريات", "type": "مكية", "verses": 60, "start_page": 520},
    {"id": 52, "name": "الطور", "type": "مكية", "verses": 49, "start_page": 523},
    {"id": 53, "name": "النجم", "type": "مكية", "verses": 62, "start_page": 526},
    {"id": 54, "name": "القمر", "type": "مكية", "verses": 55, "start_page": 528},
    {"id": 55, "name": "الرحمن", "type": "مدنية", "verses": 78, "start_page": 531},
    {"id": 56, "name": "الواقعة", "type": "مكية", "verses": 96, "start_page": 534},
    {"id": 57, "name": "الحديد", "type": "مدنية", "verses": 29, "start_page": 537},
    {"id": 58, "name": "المجادلة", "type": "مدنية", "verses": 22, "start_page": 542},
    {"id": 59, "name": "الحشر", "type": "مدنية", "verses": 24, "start_page": 545},
    {"id": 60, "name": "الممتحنة", "type": "مدنية", "verses": 13, "start_page": 549},
    {"id": 61, "name": "الصف", "type": "مدنية", "verses": 14, "start_page": 551},
    {"id": 62, "name": "الجمعة", "type": "مدنية", "verses": 11, "start_page": 553},
    {"id": 63, "name": "المنافقون", "type": "مدنية", "verses": 11, "start_page": 554},
    {"id": 64, "name": "التغابن", "type": "مدنية", "verses": 18, "start_page": 556},
    {"id": 65, "name": "الطلاق", "type": "مدنية", "verses": 12, "start_page": 558},
    {"id": 66, "name": "التحريم", "type": "مدنية", "verses": 12, "start_page": 560},
    {"id": 67, "name": "الملك", "type": "مكية", "verses": 30, "start_page": 562},
    {"id": 68, "name": "القلم", "type": "مكية", "verses": 52, "start_page": 564},
    {"id": 69, "name": "الحاقة", "type": "مكية", "verses": 52, "start_page": 566},
    {"id": 70, "name": "المعارج", "type": "مكية", "verses": 44, "start_page": 568},
    {"id": 71, "name": "نوح", "type": "مكية", "verses": 28, "start_page": 570},
    {"id": 72, "name": "الجن", "type": "مكية", "verses": 28, "start_page": 572},
    {"id": 73, "name": "المزمل", "type": "مكية", "verses": 20, "start_page": 574},
    {"id": 74, "name": "المدثر", "type": "مكية", "verses": 56, "start_page": 575},
    {"id": 75, "name": "القيامة", "type": "مكية", "verses": 40, "start_page": 577},
    {"id": 76, "name": "الإنسان", "type": "مدنية", "verses": 31, "start_page": 578},
    {"id": 77, "name": "المرسلات", "type": "مكية", "verses": 50, "start_page": 580},
    {"id": 78, "name": "النبأ", "type": "مكية", "verses": 40, "start_page": 582},
    {"id": 79, "name": "النازعات", "type": "مكية", "verses": 46, "start_page": 583},
    {"id": 80, "name": "عبس", "type": "مكية", "verses": 42, "start_page": 585},
    {"id": 81, "name": "التكوير", "type": "مكية", "verses": 29, "start_page": 586},
    {"id": 82, "name": "الانفطار", "type": "مكية", "verses": 19, "start_page": 587},
    {"id": 83, "name": "المطففين", "type": "مكية", "verses": 36, "start_page": 587},
    {"id": 84, "name": "الانشقاق", "type": "مكية", "verses": 25, "start_page": 589},
    {"id": 85, "name": "البروج", "type": "مكية", "verses": 22, "start_page": 590},
    {"id": 86, "name": "الطارق", "type": "مكية", "verses": 17, "start_page": 591},
    {"id": 87, "name": "الأعلى", "type": "مكية", "verses": 19, "start_page": 591},
    {"id": 88, "name": "الغاشية", "type": "مكية", "verses": 26, "start_page": 592},
    {"id": 89, "name": "الفجر", "type": "مكية", "verses": 30, "start_page": 593},
    {"id": 90, "name": "البلد", "type": "مكية", "verses": 20, "start_page": 594},
    {"id": 91, "name": "الشمس", "type": "مكية", "verses": 15, "start_page": 595},
    {"id": 92, "name": "الليل", "type": "مكية", "verses": 21, "start_page": 595},
    {"id": 93, "name": "الضحى", "type": "مكية", "verses": 11, "start_page": 596},
    {"id": 94, "name": "الشرح", "type": "مكية", "verses": 8, "start_page": 596},
    {"id": 95, "name": "التين", "type": "مكية", "verses": 8, "start_page": 597},
    {"id": 96, "name": "العلق", "type": "مكية", "verses": 19, "start_page": 597},
    {"id": 97, "name": "القدر", "type": "مكية", "verses": 5, "start_page": 598},
    {"id": 98, "name": "البينة", "type": "مدنية", "verses": 8, "start_page": 598},
    {"id": 99, "name": "الزلزلة", "type": "مدنية", "verses": 8, "start_page": 599},
    {"id": 100, "name": "العاديات", "type": "مكية", "verses": 11, "start_page": 599},
    {"id": 101, "name": "القارعة", "type": "مكية", "verses": 11, "start_page": 600},
    {"id": 102, "name": "التكاثر", "type": "مكية", "verses": 8, "start_page": 600},
    {"id": 103, "name": "العصر", "type": "مكية", "verses": 3, "start_page": 601},
    {"id": 104, "name": "الهمزة", "type": "مكية", "verses": 9, "start_page": 601},
    {"id": 105, "name": "الفيل", "type": "مكية", "verses": 5, "start_page": 601},
    {"id": 106, "name": "قريش", "type": "مكية", "verses": 4, "start_page": 602},
    {"id": 107, "name": "الماعون", "type": "مكية", "verses": 7, "start_page": 602},
    {"id": 108, "name": "الكوثر", "type": "مكية", "verses": 3, "start_page": 602},
    {"id": 109, "name": "الكافرون", "type": "مكية", "verses": 6, "start_page": 603},
    {"id": 110, "name": "النصر", "type": "مدنية", "verses": 3, "start_page": 603},
    {"id": 111, "name": "المسد", "type": "مكية", "verses": 5, "start_page": 603},
    {"id": 112, "name": "الإخلاص", "type": "مكية", "verses": 4, "start_page": 604},
    {"id": 113, "name": "الفلق", "type": "مكية", "verses": 5, "start_page": 604},
    {"id": 114, "name": "الناس", "type": "مكية", "verses": 6, "start_page": 604},
]

JUZ_START_PAGES = [
    1, 22, 42, 62, 82, 102, 122, 142, 162, 182,
    202, 222, 242, 262, 282, 302, 322, 342, 362, 382,
    402, 422, 442, 462, 482, 502, 522, 542, 562, 582
]

def get_juz_for_page(page: int) -> int:
    """Return Juz number (1-30) for a given page."""
    for i in range(len(JUZ_START_PAGES) - 1, -1, -1):
        if page >= JUZ_START_PAGES[i]:
            return i + 1
    return 1

def get_surahs_for_page(page: int) -> list[dict]:
    """Return all surahs present or active on a given page."""
    current_surah = None
    for s in SURAH_LIST:
        if s["start_page"] <= page:
            current_surah = s
        else:
            break
    
    # Also find if any new Surah starts on this page
    starting_here = [s for s in SURAH_LIST if s["start_page"] == page]
    if starting_here:
        return starting_here
    return [current_surah] if current_surah else [SURAH_LIST[0]]

def get_page_image_urls(page: int) -> list[str]:
    """
    روابط الصور الرسمية لمصحف المدينة النبوية (مجمع الملك فهد لطباعة المصحف الشريف)
    High-res official Madinah Mushaf scans
    """
    page_num = max(1, min(604, page))
    return [
        f"https://quran.ksu.edu.sa/png_big/{page_num}.png",
        f"https://android.quran.com/data/width_1260/page{page_num:03d}.png"
    ]

def get_audio_recitation_url(page: int) -> str:
    """رابط تلاوة مباركة للصفحة بصوت كبار القراء في المدينة المنورة"""
    return f"https://quran.ksu.edu.sa/index.php#aya={page}&p={page}"
