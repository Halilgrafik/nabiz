from django.db import migrations


CATEGORIES = [
    {'name': 'Dünya Teknoloji', 'slug': 'dunya-teknoloji'},
    {'name': 'Türkiye Teknoloji', 'slug': 'turkiye-teknoloji'},
]

SOURCES = [
    {'name': 'TechCrunch', 'feed_url': 'https://techcrunch.com/feed/', 'website_url': 'https://techcrunch.com/', 'category': 'dunya-teknoloji'},
    {'name': 'The Verge', 'feed_url': 'https://www.theverge.com/rss/index.xml', 'website_url': 'https://www.theverge.com/', 'category': 'dunya-teknoloji'},
    {'name': 'Ars Technica', 'feed_url': 'https://arstechnica.com/feed/', 'website_url': 'https://arstechnica.com/', 'category': 'dunya-teknoloji'},
    {'name': 'Wired', 'feed_url': 'https://www.wired.com/feed/rss', 'website_url': 'https://www.wired.com/', 'category': 'dunya-teknoloji'},
    {'name': 'Webrazzi', 'feed_url': 'https://webrazzi.com/kategori/teknoloji/feed', 'website_url': 'https://webrazzi.com/', 'category': 'turkiye-teknoloji'},
    {'name': 'Log.com.tr', 'feed_url': 'https://www.log.com.tr/feed/', 'website_url': 'https://www.log.com.tr/', 'category': 'turkiye-teknoloji'},
    {'name': 'ShiftDelete.Net', 'feed_url': 'https://shiftdelete.net/feed', 'website_url': 'https://shiftdelete.net/', 'category': 'turkiye-teknoloji'},
    {'name': 'DonanımHaber', 'feed_url': 'https://www.donanimhaber.com/rss/tum/', 'website_url': 'https://www.donanimhaber.com/', 'category': 'turkiye-teknoloji'},
]


def seed(apps, schema_editor):
    Category = apps.get_model('news', 'Category')
    Source = apps.get_model('news', 'Source')

    slug_to_category = {}
    for cat in CATEGORIES:
        obj, _ = Category.objects.get_or_create(slug=cat['slug'], defaults={'name': cat['name']})
        slug_to_category[cat['slug']] = obj

    for src in SOURCES:
        Source.objects.get_or_create(
            feed_url=src['feed_url'],
            defaults={
                'name': src['name'],
                'website_url': src['website_url'],
                'category': slug_to_category[src['category']],
                'is_active': True,
            },
        )


def unseed(apps, schema_editor):
    Source = apps.get_model('news', 'Source')
    Category = apps.get_model('news', 'Category')
    Source.objects.filter(feed_url__in=[s['feed_url'] for s in SOURCES]).delete()
    Category.objects.filter(slug__in=[c['slug'] for c in CATEGORIES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
