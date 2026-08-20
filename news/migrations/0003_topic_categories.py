from django.db import migrations, models


TOPIC_KEYWORDS = {
    'yapay-zeka': (
        'Yapay Zeka',
        [
            'yapay zeka', 'yapay zekâ', 'artificial intelligence', 'chatgpt', 'openai',
            'gpt-', 'gpt ', 'llm', 'machine learning', 'makine öğrenmesi', 'gemini',
            'claude', 'anthropic', 'copilot', 'neural network', 'chatbot', 'genai',
            'generative ai', 'yapay zekâ modeli', 'yapay zeka modeli', 'deep learning',
        ],
    ),
    'telefon-cihazlar': (
        'Telefon & Cihazlar',
        [
            'iphone', 'samsung galaxy', 'galaxy s', 'android telefon', 'smartphone',
            'akıllı telefon', 'xiaomi', 'huawei', 'oppo', 'realme', 'oneplus', 'pixel ',
            'akıllı saat', 'smartwatch', 'kulaklık', 'earbuds', 'tablet', 'wearable',
        ],
    ),
    'grafik-tasarim': (
        'Grafik Tasarım',
        [
            'photoshop', 'illustrator', 'figma', 'adobe', 'grafik tasarım', 'ui/ux',
            'ux tasarım', 'tipografi', 'font tasarımı', 'canva', 'logo tasarım',
            'creative cloud', 'indesign',
        ],
    ),
    'saglik-teknolojisi': (
        'Sağlık Teknolojisi',
        [
            'sağlık teknolojisi', 'tıbbi', 'medikal', 'health tech', 'biotech',
            'biyoteknoloji', 'ilaç geliştirme', 'hastane', 'klinik araştırma',
            'fda onay', 'wearable health', 'genetik', 'aşısı', 'aşı çalışması',
            'tedavi teknolojisi',
        ],
    ),
    'sosyal-medya': (
        'Sosyal Medya',
        [
            'instagram', 'tiktok', 'twitter', 'facebook', 'meta platforms',
            'sosyal medya', 'youtube', 'snapchat', 'whatsapp', 'threads uygulaması',
            'linkedin',
        ],
    ),
}

FALLBACK_SLUG = 'genel-teknoloji'
FALLBACK_NAME = 'Genel Teknoloji'

OLD_CATEGORY_SLUGS = ['dunya-teknoloji', 'turkiye-teknoloji']


def classify_slug(title, summary):
    text = f'{title} {summary}'.lower()
    best_slug = FALLBACK_SLUG
    best_score = 0
    for slug, (_, keywords) in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > best_score:
            best_score = score
            best_slug = slug
    return best_slug


def recategorize(apps, schema_editor):
    Category = apps.get_model('news', 'Category')
    Article = apps.get_model('news', 'Article')

    categories = {}
    for slug, (name, _) in TOPIC_KEYWORDS.items():
        category, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name})
        categories[slug] = category
    fallback, _ = Category.objects.get_or_create(slug=FALLBACK_SLUG, defaults={'name': FALLBACK_NAME})
    categories[FALLBACK_SLUG] = fallback

    for article in Article.objects.all():
        slug = classify_slug(article.title, article.summary)
        article.category = categories[slug]
        article.save(update_fields=['category'])

    Category.objects.filter(slug__in=OLD_CATEGORY_SLUGS).delete()


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_seed_sources'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source',
            name='category',
        ),
        migrations.RunPython(recategorize, reverse_noop),
    ]
