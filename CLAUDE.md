# Nabız — Proje Yönergesi

Teknoloji haberlerini RSS ile otomatik toplayan, koyu temalı, kişisel "okuma nabzı" paneli olan bir haber okuyucu. Plan dosyası: `~/.claude/plans/sparkling-hopping-gosling.md` (fazların tam gerekçesi ve tasarım kararları orada).

**Geliştirici: Başlangıç seviyesi** — açıklamalar ve production'a dokunan adımlarda (env var, deploy, git push) açık ve dikkatli olunmalı.

## Proje Özeti

Herkes giriş yapmadan haberleri gezebilir, kategoriye göre filtreleyebilir, orijinal kaynağa tıklayabilir. Giriş yapan kullanıcıların hangi haberleri okuduğu kaydedilir (`ReadEvent`) ve `/nabiz/` panelinde toplam okuma, kategori dağılımı, günlük seri (streak) ve son 14 günün grafiği olarak gösterilir. Amaç: kullanıcının yıllar içinde teknolojiyle bağının nasıl geliştiğini kendi gözünde somutlaştırmak.

## Teknoloji Yığını

Diğer Django/Railway projeleriyle (`-r-n-fiyat-i-in-proje`, `Not-Defterim`) aynı desen: Django + `python-dotenv` (env okuma) + manuel `DATABASE_URL` ayrıştırma (sqlite yerelde, postgres Railway'de) + Whitenoise (statik dosyalar) + Gunicorn + Nixpacks (`Procfile`/`railway.json`/`start.sh`).

## Uygulama Yapısı

- `core/` — paylaşılan/site geneli görünümler (kayıt formu `core/views.py::register`)
- `news/` — asıl uygulama: `Category`, `Source`, `Article`, `ReadEvent` modelleri; `article_list`/`read_article`/`dashboard` view'ları; `fetch_news` yönetim komutu
- `templates/` (proje kökü) — `base.html` (koyu tema), `registration/login.html`, `registration/register.html`, `404.html`, `500.html`, `robots.txt`
- `static/css/style.css` — tüm koyu tema stilleri, framework yok

## FAZ 0 — Proje İskeleti ✅ TAMAMLANDI

Django projesi + `core`/`news` app'leri oluşturuldu, `.env`/`.gitignore`, Railway deploy dosyaları (`Procfile`, `railway.json`, `start.sh`) diğer projelerden birebir kopyalandı (sadece wsgi modülü `nabiz.wsgi` olarak değişti).

## FAZ 1 — Veri Modeli + RSS Toplama ✅ TAMAMLANDI

- `news/models.py`: `Category`, `Source` (feed_url + kategori + `is_active`), `Article` (link/guid ile tekilleştirme), `ReadEvent`
- `news/management/commands/fetch_news.py`: aktif kaynakları gezip `requests` + `feedparser` ile çeker, kaynak başına `try/except` (bir kaynak bozuksa diğerleri etkilenmez), `link`/`guid` ile tekrar eklemeyi engeller
- `news/migrations/0002_seed_sources.py`: 8 başlangıç kaynağı (4 uluslararası: TechCrunch, The Verge, Ars Technica, Wired · 4 yerli: Webrazzi, Log.com.tr, ShiftDelete.Net, DonanımHaber) — tüm feed URL'leri bu oturumda gerçekten `curl` ile doğrulandı, çalışıyor
- Doğrulandı: ilk çalıştırmada 195 gerçek haber çekildi, ikinci çalıştırmada 0 yeni/195 atlandı (dedupe çalışıyor)
- Yeni kaynak eklemek kod değişikliği gerektirmez — `/admin/news/source/` üzerinden eklenir, `is_active` ile açılıp kapatılabilir

## FAZ 2 — Herkese Açık Okuma Arayüzü ✅ TAMAMLANDI

`/` — kategori filtreli (`?category=<slug>`), sayfalanmış haber listesi, koyu tema. Haberler kendi özetiyle gösteriliyor, tıklanınca orijinal kaynağa yönlendiriyor (tam metin scrape edilmiyor — telif/etik gerekçesiyle bilinçli tercih, plan dosyasında detaylı gerekçe var).

## FAZ 3 — Kayıt/Giriş + Okuma Takibi ✅ TAMAMLANDI

Django'nun yerleşik auth view'ları (`django.contrib.auth.urls`) + `core/views.py::register` (custom, `UserCreationForm`). `/read/<id>/` view'ı: giriş yapmış kullanıcı için `ReadEvent` oluşturup orijinal linke 302 yönlendiriyor; anonim kullanıcı direkt yönlendiriliyor (okuma geziniminde login zorunluluğu yok).

## FAZ 4 — "Nabız" İstatistik Paneli ✅ TAMAMLANDI

`/nabiz/` (`@login_required`): toplam/haftalık/aylık okuma sayısı, kategori dağılımı, günlük seri (`ReadEvent` tarihleri üzerinden Python'da hesaplanıyor — SQL window function yerine okunabilirlik tercih edildi), son 14 günün Chart.js (CDN) grafiği.

Uçtan uca test edildi (bu oturumda, `curl` ile): kayıt → otomatik giriş → habere tıkla → `ReadEvent` oluştu → panelde doğru sayılar göründü (1 okuma, 1 seri).

## FAZ 5 — Cila + Yayına Alma 🔶 KISMEN TAMAMLANDI

Yapılanlar: `README.md`, `LICENSE` (MIT), `robots.txt`, 404/500 sayfaları, `.env.example`.

**Kalan (kullanıcı tarafından yapılmalı — Claude Code'un erişemediği adımlar):**
1. Railway'de yeni proje oluştur, GitHub reposunu (`Halilgrafik/nabiz`) bağla
2. Aynı projeye **PostgreSQL eklentisi** ekle
3. Ortam değişkenleri: `SECRET_KEY` (yeni/rastgele, yerel `.env`'dekiyle aynı olmasın), `DEBUG=False`, `ALLOWED_HOSTS` (Railway'in verdiği `*.up.railway.app` adresi), `CSRF_TRUSTED_ORIGINS` (`https://...` tam adres)
4. Deploy sonrası bir kerelik `python manage.py createsuperuser` çalıştır (Railway konsolundan veya `railway run`)
5. Haber çekmeyi otomatikleştirmek için: aynı projede başlangıç komutu `python manage.py fetch_news` olan **ikinci bir servis** oluştur, Settings → Cron Schedule'a `0 * * * *` (saatlik, UTC) gir. Bu servis gunicorn/port'a ihtiyaç duymaz, sadece komutu çalıştırıp çıkar.
6. (Opsiyonel) Özel domain bağlanacaksa Railway'in domain ayarlarından yapılır.

## İleride, Şimdi Değil (kapsam dışı bırakıldı)

- Reddit API entegrasyonu (OAuth + rate limit karmaşıklığı)
- X/Twitter entegrasyonu (API artık ücretli)
- Quiz/puanlama tarzı "teknolojiye yakınlık" ölçümü (basit okuma istatistiğine karar verildi)
- Okunmamış haberler için e-posta özeti

## Sıradaki Adım

Kod tarafı (Faz 0-4 ve Faz 5'in yerel kısmı) tamamlandı ve yerelde uçtan uca doğrulandı. Bir sonraki adım kullanıcının Railway'de projeyi oluşturup yukarıdaki FAZ 5 adımlarını tamamlaması. Railway CLI bu makinede kurulu değil ve `railway login` tarayıcı üzerinden interaktif kimlik doğrulama gerektirdiğinden, bu adım Claude Code tarafından otomatikleştirilemez.
