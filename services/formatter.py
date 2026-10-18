"""
محرر التنسيق الجمالي الإسلامي لمنشورات التيليجرام
تنسيق فخم ومهيب يليق بكتاب الله والأذكار النبوية الشريفة
"""

def to_arabic_num(number: int) -> str:
    """تحويل الأرقام إلى الأرقام العربية المشرقية"""
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    return "".join(arabic_digits[int(d)] if d.isdigit() else d for d in str(number))

def format_quran_wird_caption(
    page: int,
    surah_name: str,
    juz: int,
    verse_range: str = "",
    tafsir_snippet: str = ""
) -> str:
    """تنسيق كابشن ورد القرآن الكريم اليومي (مصحف المدينة النبوية - مجمع الملك فهد)"""
    ar_page = to_arabic_num(page)
    ar_juz = to_arabic_num(juz)
    
    caption = (
        "<b>📖 ━━━━━━━━━━━━━━━━━━━</b>\n"
        "<b>✨ ورد القرآن الكريم اليومي ✨</b>\n"
        "<i>﴿ مصحف المدينة النبوية - مجمع الملك فهد ﴾</i>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        f"📍 <b>الصفحة:</b> {ar_page}  |  <b>الجزء:</b> {ar_juz}\n"
        f"🕌 <b>السورة الكريمة:</b> سورة {surah_name}\n"
    )
    if verse_range:
        caption += f"🔢 <b>الآيات:</b> {verse_range}\n"
    
    if tafsir_snippet:
        caption += (
            f"\n💡 <b>قبس من التفسير الميسر:</b>\n"
            f"<blockquote>{tafsir_snippet}</blockquote>\n"
        )
    
    caption += (
        f"\n🎧 <a href='https://quran.ksu.edu.sa/index.php#aya={page}&p={page}'><b>استمع لتلاوة الصفحة بصوت كبار أئمة الحرمين</b></a>\n\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n"
        "🌱 <i>اجعل للقرآن نصيباً من يومك، فإنه يأتي يوم القيامة شفيعاً لأصحابه.</i>\n\n"
        "#ورد_القرآن #مصحف_المدينة #مجمع_الملك_فهد #تلاوة"
    )
    return caption

def format_adhkar_sabah_post(adhkar_list: list[dict]) -> str:
    """تنسيق رسالة أذكار الصباح المباركة"""
    msg = (
        "<b>☀️ ━━━━━━━━━━━━━━━━━━━</b>\n"
        "<b>✨ أذكار الصباح المباركة ✨</b>\n"
        "<i>﴿ مأثورة وصحيحة عن النبي ﷺ ﴾</i>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
    )
    for idx, item in enumerate(adhkar_list, 1):
        ar_idx = to_arabic_num(idx)
        rep = item['repeat']
        rep_text = "مرة واحدة" if rep == 1 else f"{rep} مرات" if rep <= 10 else f"{rep} مرة"
        
        msg += (
            f"<b>{ar_idx}. {item['title']}</b> <i>({rep_text})</i>\n"
            f"<blockquote>{item['text']}</blockquote>\n"
            f"📜 <i>{item['source']}</i>\n"
            f"💫 <b>الفضل:</b> {item['virtue']}\n\n"
            "───────────────\n\n"
        )
        # Avoid exceeding Telegram single message limit (4096 chars)
        if len(msg) > 3200:
            break
            
    msg += (
        "🌱 <i>«مَنْ صَلَّى الْفَجْرَ فَهُوَ فِي ذِمَّةِ اللَّهِ»</i>\n"
        "#أذكار_الصباح #حصن_المسلم #السنة_النبوية"
    )
    return msg

def format_adhkar_masa_post(adhkar_list: list[dict]) -> str:
    """تنسيق رسالة أذكار المساء المباركة"""
    msg = (
        "<b>🌙 ━━━━━━━━━━━━━━━━━━━</b>\n"
        "<b>✨ أذكار المساء المباركة ✨</b>\n"
        "<i>﴿ مأثورة وصحيحة عن النبي ﷺ ﴾</i>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
    )
    for idx, item in enumerate(adhkar_list, 1):
        ar_idx = to_arabic_num(idx)
        rep = item['repeat']
        rep_text = "مرة واحدة" if rep == 1 else f"{rep} مرات" if rep <= 10 else f"{rep} مرة"
        
        msg += (
            f"<b>{ar_idx}. {item['title']}</b> <i>({rep_text})</i>\n"
            f"<blockquote>{item['text']}</blockquote>\n"
            f"📜 <i>{item['source']}</i>\n"
            f"💫 <b>الفضل:</b> {item['virtue']}\n\n"
            "───────────────\n\n"
        )
        if len(msg) > 3200:
            break
            
    msg += (
        "🌱 <i>حصن نفسك وأهلك بأذكار المساء تكن في حفظ الله ورعايته حتى تصبح.</i>\n"
        "#أذكار_المساء #حصن_المسلم #السنة_النبوية"
    )
    return msg

def format_adhkar_nawm_post(adhkar_list: list[dict]) -> str:
    """تنسيق أذكار النوم الصحيحة"""
    msg = (
        "<b>🌌 ━━━━━━━━━━━━━━━━━━━</b>\n"
        "<b>✨ سنن وأذكار النوم الصحيحة ✨</b>\n"
        "<i>﴿ ختام ليلتك على الفطرة وسنة المصطفى ﷺ ﴾</i>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
    )
    for idx, item in enumerate(adhkar_list, 1):
        ar_idx = to_arabic_num(idx)
        msg += (
            f"<b>{ar_idx}. {item['title']}</b>\n"
            f"<blockquote>{item['text']}</blockquote>\n"
            f"📜 <i>{item['source']}</i>\n"
            f"💫 <b>الفضل:</b> {item['virtue']}\n\n"
            "───────────────\n\n"
        )
    msg += (
        "🌙 <i>توضأ قبل نومك وانفض فراشك واجعل آخر كلامك ذكراً لله تعالى.</i>\n"
        "#أذكار_النوم #السنة_النبوية #نوم_على_الفطرة"
    )
    return msg

def format_witr_reminder(item: dict) -> str:
    """تنسيق تذكير صلاة الوتر وقيام الليل في جوف الليل الأخير"""
    return (
        "<b>🕋 ━━━━━━━━━━━━━━━━━━━</b>\n"
        f"<b>{item['title']}</b>\n"
        "<i>﴿ بتوقيت مكة المكرمة - ثلث الليل الأخير ﴾</i>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        f"<blockquote>{item['hadith']}</blockquote>\n"
        f"📜 <i>{item['source']}</i>\n\n"
        f"🤍 <b>رسالة لك:</b>\n"
        f"{item['action']}\n\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n"
        "✨ <i>قال تعالى: ﴿وَبِالْأَسْحَارِ هُمْ يَسْتَغْفِرُونَ﴾</i>\n"
        "#صلاة_الوتر #قيام_الليل #استغفار_الأسحار #مكة_المكرمة"
    )

def format_prayer_table_post(hijri_date: str, gregorian_date: str, timings: dict) -> str:
    """تنسيق بطاقة مواقيت الصلاة اليومية في مكة المكرمة (تقويم أم القرى)"""
    return (
        "<b>🕋 ━━━━━━━━━━━━━━━━━━━</b>\n"
        "<b>✨ مواقيت الصلاة في مكة المكرمة ✨</b>\n"
        "<i>﴿ وفق تقويم أم القرى الرسمي بالمملكة العربية السعودية ﴾</i>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        f"📅 <b>التاريخ الهجري:</b> {hijri_date}\n"
        f"🗓️ <b>التاريخ الميلادي:</b> {gregorian_date}\n\n"
        "<b>جدول المواقيت اليوم:</b>\n"
        f"▫️ <b>الفجر:</b>  <code>{timings.get('Fajr', '--:--')}</code>\n"
        f"▫️ <b>الشروق:</b> <code>{timings.get('Sunrise', '--:--')}</code>\n"
        f"▫️ <b>الظهر:</b>  <code>{timings.get('Dhuhr', '--:--')}</code>\n"
        f"▫️ <b>العصر:</b>  <code>{timings.get('Asr', '--:--')}</code>\n"
        f"▫️ <b>المغرب:</b> <code>{timings.get('Maghrib', '--:--')}</code>\n"
        f"▫️ <b>العشاء:</b> <code>{timings.get('Isha', '--:--')}</code>\n\n"
        f"🌙 <b>ثلث الليل الأخير (الوتر):</b> <code>{timings.get('Lastthird', '02:00')}</code>\n\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n"
        "🌱 <i>«إِنَّ الصَّلَاةَ كَانَتْ عَلَى الْمُؤْمِنِينَ كِتَابًا مَّوْقُوتًا»</i>\n"
        "#مواقيت_الصلاة #مكة_المكرمة #تقويم_أم_القرى"
    )

def format_azan_reminder(prayer_name: str, prayer_time: str) -> str:
    """تنسيق تنبيه الأذان ودخول وقت الفريضة بتوقيت مكة المكرمة"""
    return (
        "<b>🕋 ━━━━━━━━━━━━━━━━━━━</b>\n"
        f"<b>📢 حان الآن أذان {prayer_name}</b>\n"
        f"<i>﴿ حسب توقيت مكة المكرمة: {prayer_time} ﴾</i>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        "حي على الصلاة.. حي على الفلاح 🌿\n\n"
        "<b>🤲 دعاء ما بعد الأذان المستجاب:</b>\n"
        "<blockquote>«اللَّهُمَّ رَبَّ هَذِهِ الدَّعْوَةِ التَّامَّةِ، وَالصَّلاَةِ الْقَائِمَةِ، آتِ مُحَمَّداً الْوَسِيلَةَ وَالْفَضِيلَةَ، وَابْعَثْهُ مَقَاماً مَحْمُوداً الَّذِي وَعَدْتَهُ».</blockquote>\n"
        "📜 <i>رواه البخاري (614) - تحل له شفاعة النبي ﷺ يوم القيامة</i>\n\n"
        "💡 <i>بادر بالوضوء وإجابة النداء، والصلاة في وقتها أحب الأعمال إلى الله.</i>\n\n"
        f"#أذان_{prayer_name} #صلاة_{prayer_name} #مكة_المكرمة"
    )

def format_duha_reminder() -> str:
    """تنسيق تذكير صلاة الضحى (صلاة الأوابين)"""
    return (
        "<b>☀️ ━━━━━━━━━━━━━━━━━━━</b>\n"
        "<b>🕊️ تذكير بصلاة الضحى (صلاة الأوابين)</b>\n"
        "<i>﴿ صدقة عن كل مفصل من مفاصل جسدك ﴾</i>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        "<blockquote>قال رسول الله ﷺ: «يُصْبِحُ عَلَى كُلِّ سُلاَمَى مِنْ أَحَدِكُمْ صَدَقَةٌ... وَيُجْزِئُ مِنْ ذَلِكَ رَكْعَتَانِ يَرْكَعُهُمَا مِنَ الضُّحَى».</blockquote>\n"
        "📜 <i>صحيح مسلم (720)</i>\n\n"
        "🌿 <b>وقتها:</b> يبدأ بعد شروق الشمس بربع ساعة، ويمتد إلى قبل أذان الظهر بعشر دقائق.\n"
        "🤍 ركعتان خفيفتان تشكر بهما نعم الله عليك وتكتب بهما من الأوابين.\n\n"
        "#صلاة_الضحى #صلاة_الأوابين #سنة_نبوية"
    )

def format_friday_kahf_post(kahf_data: dict) -> str:
    """تنسيق منشور سورة الكهف يوم الجمعة"""
    return (
        "<b>✨ ━━━━━━━━━━━━━━━━━━━</b>\n"
        f"<b>{kahf_data['title']}</b>\n"
        "<i>﴿ يوم الجمعة المبارك ﴾</i>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        f"<blockquote>{kahf_data['hadith']}</blockquote>\n"
        f"📜 <i>{kahf_data['source']}</i>\n\n"
        f"📖 <a href='{kahf_data['link']}'><b>اضغط هنا لقراءة سورة الكهف كاملة بتنسيق المصحف</b></a>\n\n"
        f"💡 {kahf_data['advice']}\n\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n"
        "#سورة_الكهف #يوم_الجمعة #نور_ما_بين_الجمعتين"
    )

def format_friday_salawat_post(salawat_data: dict) -> str:
    """تنسيق منشور الصلاة على النبي ﷺ يوم الجمعة"""
    return (
        "<b>✨ ━━━━━━━━━━━━━━━━━━━</b>\n"
        f"<b>{salawat_data['title']}</b>\n"
        "<i>﴿ أكثروا عليّ من الصلاة فيه ﴾</i>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        f"<blockquote>{salawat_data['hadith']}</blockquote>\n"
        f"📜 <i>{salawat_data['source']}</i>\n\n"
        f"🤲 <b>الصيغة الإبراهيمية المباركة:</b>\n"
        f"<blockquote>{salawat_data['salat_text']}</blockquote>\n\n"
        f"🤍 {salawat_data['advice']}\n\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n"
        "#الصلاة_على_النبي #يوم_الجمعة #سنة_نبوية"
    )

def format_friday_istijaba_post(istijaba_data: dict) -> str:
    """تنسيق منشور ساعة الإجابة عصر الجمعة"""
    return (
        "<b>🤲 ━━━━━━━━━━━━━━━━━━━</b>\n"
        f"<b>{istijaba_data['title']}</b>\n"
        "<i>﴿ بين العصر والمغرب - أرجى أوقات الإجابة ﴾</i>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        f"<blockquote>{istijaba_data['hadith']}</blockquote>\n"
        f"📜 <i>{istijaba_data['source']}</i>\n\n"
        f"💫 {istijaba_data['advice']}\n\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n"
        "#ساعة_الإجابة #عصر_الجمعة #دعاء_مستجاب"
    )

def format_daily_dua_post(dua_item: dict) -> str:
    """تنسيق منشور دعاء اليوم المأثور"""
    return (
        "<b>🤲 ━━━━━━━━━━━━━━━━━━━</b>\n"
        "<b>✨ دعاء اليوم المأثور من جوامع كلمه ﷺ ✨</b>\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        f"<b>{dua_item['title']}:</b>\n\n"
        f"<blockquote>{dua_item['dua']}</blockquote>\n"
        f"📜 <i>{dua_item['source']}</i>\n\n"
        "<b>━━━━━━━━━━━━━━━━━━━━━</b>\n"
        "🤍 <i>ردد هذا الدعاء بيقين واستحضر معانيه العظيمة في يومك.</i>\n"
        "#دعاء_اليوم #جوامع_الدعاء #السنة_النبوية"
    )
