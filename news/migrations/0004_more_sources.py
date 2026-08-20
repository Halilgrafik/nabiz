from django.db import migrations


NEW_SOURCES = [
    # Uluslararası — genel teknoloji
    {'name': 'Engadget', 'feed_url': 'https://www.engadget.com/rss.xml', 'website_url': 'https://www.engadget.com/'},
    {'name': 'BBC Technology', 'feed_url': 'http://feeds.bbci.co.uk/news/technology/rss.xml', 'website_url': 'https://www.bbc.com/news/technology'},
    {'name': 'ZDNet', 'feed_url': 'https://www.zdnet.com/news/rss.xml', 'website_url': 'https://www.zdnet.com/'},
    {'name': 'MIT Technology Review', 'feed_url': 'https://www.technologyreview.com/feed/', 'website_url': 'https://www.technologyreview.com/'},
    {'name': 'VentureBeat', 'feed_url': 'https://venturebeat.com/feed/', 'website_url': 'https://venturebeat.com/'},
    {'name': 'Mashable', 'feed_url': 'https://mashable.com/feeds/rss/all', 'website_url': 'https://mashable.com/'},
    # Telefon & cihaz odaklı
    {'name': '9to5Mac', 'feed_url': 'https://9to5mac.com/feed/', 'website_url': 'https://9to5mac.com/'},
    {'name': 'Android Authority', 'feed_url': 'https://www.androidauthority.com/feed/', 'website_url': 'https://www.androidauthority.com/'},
    # Grafik tasarım odaklı
    {'name': 'Creative Bloq', 'feed_url': 'https://www.creativebloq.com/feed', 'website_url': 'https://www.creativebloq.com/'},
    {'name': 'Smashing Magazine', 'feed_url': 'https://www.smashingmagazine.com/feed', 'website_url': 'https://www.smashingmagazine.com/'},
    # Sağlık teknolojisi odaklı
    {'name': 'STAT News', 'feed_url': 'https://www.statnews.com/feed/', 'website_url': 'https://www.statnews.com/'},
    # Türkiye — büyük, editöryel haber kuruluşları
    {'name': 'Webtekno', 'feed_url': 'https://www.webtekno.com/rss.xml', 'website_url': 'https://www.webtekno.com/'},
    {'name': 'Chip Türkiye', 'feed_url': 'https://www.chip.com.tr/rss', 'website_url': 'https://www.chip.com.tr/'},
    {'name': 'NTV Teknoloji', 'feed_url': 'https://www.ntv.com.tr/teknoloji.rss', 'website_url': 'https://www.ntv.com.tr/teknoloji'},
]


def seed(apps, schema_editor):
    Source = apps.get_model('news', 'Source')
    for src in NEW_SOURCES:
        Source.objects.get_or_create(
            feed_url=src['feed_url'],
            defaults={
                'name': src['name'],
                'website_url': src['website_url'],
                'is_active': True,
            },
        )


def unseed(apps, schema_editor):
    Source = apps.get_model('news', 'Source')
    Source.objects.filter(feed_url__in=[s['feed_url'] for s in NEW_SOURCES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_topic_categories'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
