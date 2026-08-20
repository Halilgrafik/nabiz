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

## FAZ 5 — Cila + Yayına Alma ✅ TAMAMLANDI (domain/superuser hariç)

Yapılanlar: `README.md`, `LICENSE` (MIT), `robots.txt`, 404/500 sayfaları, `.env.example`.

**Railway'de canlı** (2026-08-20, bu oturumda tamamlandı): proje `nabiz`, iki servis:
- **web** — `Halilgrafik/nabiz`'den `railway up` ile deploy edildi (GitHub App entegrasyonu bu hesap için yetkilendirilmediğinden `--repo` ile bağlanamadı, CLI'nin lokal kaynak yükleme yolu kullanıldı). Canlı adres: **https://web-production-d48e7.up.railway.app/**. Env: `SECRET_KEY` (yeni/rastgele), `DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DATABASE_URL=${{Postgres.DATABASE_URL}}`.
- **fetch-news** — aynı kod, ayrı bir Railway config dosyası kullanıyor: `railway.cron.json` (`startCommand: python manage.py fetch_news`). **Önemli:** `web`'in `railway.json`'ındaki `deploy.startCommand` proje genelinde varsayılan olduğundan, aynı repodan deploy edilen her servise uygulanıyor — cron servisine ayrı `railwayConfigFile` (`serviceInstanceUpdate` mutasyonuyla) atanmadan `bash start.sh`/gunicorn çalıştırmaya devam ediyordu. Bu yüzden ikinci bir servis eklerken mutlaka kendi config dosyasını ata. Cron schedule: `0 * * * *` (saatlik, UTC) — `nextCronRunAt` alanından doğrulanabilir. İlk manuel tetiklemede (`deploymentInstanceExecutionCreate` mutasyonu) 195 gerçek haber çekildi, production'da görünüyor.
- **Postgres** eklentisi ekli, `DATABASE_URL` referans değişkeni ile bağlı.

**Railway CLI notları (gelecekte bu proje üzerinde çalışırken):**
- CLI `~/.railway/bin/railway`'de kurulu, `source "$HOME/.railway/env"` ile PATH'e alınıyor.
- `railway ssh` bu WSL ortamında host-key doğrulamasında takılıyor (askpass/DISPLAY sorunu, çözülemedi) — tek seferlik yönetim komutları için `railway api` üzerinden GraphQL mutasyonları (örn. `deploymentInstanceExecutionCreate`) veya geçici env var + servis config değişikliği tercih edildi.
- `railway add --repo ...` bu GitHub hesabı için "You do not have access to this resource" hatası verdi (Railway'in GitHub App'i bu repoya yetkilendirilmemiş) — bunun yerine boş servis oluşturup `railway up` ile lokal kaynaktan deploy edildi. GitHub push sonrası otomatik deploy istenirse, Railway dashboard'undan GitHub App'e bu repo için erişim verilmesi gerekir.

**Superuser oluşturuldu** (2026-08-20): Railway dashboard'unda bu sürümde tarayıcı-içi bir shell/terminal seçeneği yok (Deploy Logs ekranındaki `...` menüsünde sadece Restart/Redeploy/Remove var, Details sekmesinde de terminal yok) — bu yüzden `railway ssh`'ın host-key sorunu nedeniyle çalışmadığı bu ortamda, geçici bir çözüm kullanıldı: `railway.createsuperuser.json` (repo köküne eklendi, `startCommand: python manage.py createsuperuser --noinput`) oluşturulup `fetch-news` servisi (canlı `web`'e dokunmadan) geçici olarak buna yönlendirildi, `DJANGO_SUPERUSER_USERNAME`/`_EMAIL`/`_PASSWORD` env değişkenleriyle çalıştırılıp sonra hem config hem env değişkenleri `railway.cron.json`/normal cron'a geri döndürüldü. `/admin/` girişi kullanıcı adı `halilgrafik` ile doğrulandı, çalışıyor. Aynı yöntem ileride başka bir yönetim komutu (`changepassword`, `loaddata` vb.) çalıştırmak gerekirse tekrar kullanılabilir — `railway.createsuperuser.json` dosyası bu amaçla repoda bırakıldı (dosyanın kendisinde şifre yok, `startCommand`'i değiştirip tekrar kullanılabilir).

**Kalan (opsiyonel, kullanıcı isterse):**
1. Özel domain bağlanacaksa Railway'in domain ayarlarından yapılır.
2. GitHub'a her push'ta otomatik deploy istenirse, Railway'in GitHub App'ine `Halilgrafik/nabiz` reposu için erişim verilip `web` servisinin source'u repoya bağlanmalı (`railway service source connect --repo Halilgrafik/nabiz --service web`).

## İleride, Şimdi Değil (kapsam dışı bırakıldı)

- Reddit API entegrasyonu (OAuth + rate limit karmaşıklığı)
- X/Twitter entegrasyonu (API artık ücretli)
- Quiz/puanlama tarzı "teknolojiye yakınlık" ölçümü (basit okuma istatistiğine karar verildi)
- Okunmamış haberler için e-posta özeti

## Sıradaki Adım

Proje Railway'de canlı ve gerçek verilerle çalışıyor (https://web-production-d48e7.up.railway.app/). Kalan tek önemli adım: `/admin/` erişimi için bir superuser hesabı oluşturmak (yukarıda FAZ 5'te detaylı).
