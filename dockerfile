# Python tabanlı bir görüntü kullan
FROM python:3.10-slim

# Sisteme ffmpeg ve gerekli kütüphaneleri kur
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    apt-get clean

# Çalışma dizini oluştur
WORKDIR /app

# Gereksinim dosyasını ve bot dosyasını ekle
COPY requirements.txt .
COPY alya_bot.py .

# Python paketlerini kur
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Uygulama çalıştırma komutu
CMD ["python", "alya_bot.py"]
