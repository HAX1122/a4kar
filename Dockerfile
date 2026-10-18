FROM python:3.12-slim

# ضبط المنطقة الزمنية ومتغيرات بايثون
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Riyadh \
    PORT=8080

WORKDIR /app

# تثبيت حزم النظام اللازمة للمنطقة الزمنية والشهادات
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    ca-certificates \
    curl \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

# نسخ وتثبيت الاعتماديات البرمجية
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كود البوت
COPY . .

# المنفذ الخاص بخادم الفحص الصحي السحابي
EXPOSE 8080

# تشغيل البوت
CMD ["python", "main.py"]
