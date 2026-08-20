# Nabız

Dünya ve Türkiye teknoloji haberlerini tek yerden takip eden, koyu temalı bir haber okuyucu. RSS kaynaklarından otomatik haber çeker; giriş yapan kullanıcılar için okuma alışkanlığını ("nabzını") gösteren kişisel bir istatistik paneli sunar.

> "Nabzını tutmak" — teknolojiyle bağını koparmadan güncel kalmak için kişisel bir araç.

## Özellikler

- **Otomatik haber toplama** — TechCrunch, The Verge, Ars Technica, Wired gibi uluslararası ve Webrazzi, Log.com.tr, ShiftDelete.Net, DonanımHaber gibi yerli kaynaklardan RSS ile, tekrarsız (dedupe'lu) şekilde.
- **Giriş yapmadan gezinme** — herkes haberleri görebilir, kategoriye göre filtreleyebilir, orijinal kaynağa tıklayabilir.
- **Kişisel "Nabız" paneli** — giriş yapan kullanıcılar için toplam okuma sayısı, haftalık/aylık okuma, kategori dağılımı, günlük okuma serisi (streak) ve son 14 günün grafiği.
- **Koyu tema**, mobil uyumlu, framework'süz sade CSS.

## Teknoloji

Django · PostgreSQL (prod) / SQLite (yerel) · Whitenoise · Gunicorn · Railway · feedparser

## Yerel Kurulum

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # SECRET_KEY'i kendi rastgele değerinle değiştir

python manage.py migrate
python manage.py fetch_news      # kaynaklardan ilk haberleri çek
python manage.py createsuperuser # /admin/ için (opsiyonel)
python manage.py runserver
```

`http://127.0.0.1:8000/` adresinde ana sayfa açılır.

Haberleri periyodik güncellemek için `python manage.py fetch_news` komutunu tekrar çalıştırman yeterli — zaten var olan haberleri tekrar eklemez.

## Kaynak Ekleme/Yönetme

Yeni bir RSS kaynağı eklemek kod değişikliği gerektirmez: `/admin/news/source/` üzerinden yeni bir `Source` kaydı oluştur (feed URL'si + kategori). Bozuk/geçici olarak çalışmayan bir kaynağı `is_active` kutucuğunu kapatarak devre dışı bırakabilirsin.

## Deployment (Railway)

- `Procfile` / `railway.json` / `start.sh` ile Nixpacks üzerinden deploy edilir (migrate → collectstatic → gunicorn).
- Ortam değişkenleri: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `DATABASE_URL` (Postgres eklentisi otomatik sağlar), `CSRF_TRUSTED_ORIGINS`.
- Haber çekme, aynı Railway projesinde başlangıç komutu `python manage.py fetch_news` olan ikinci bir servis + Cron Schedule (örn. `0 * * * *`, saatlik) ile otomatikleştirilir.

## Lisans

MIT — bkz. [LICENSE](LICENSE).
