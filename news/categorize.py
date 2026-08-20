"""Haber başlığı/özetindeki anahtar kelimelere göre kategori tahmini.

Kaynağa değil haberin içeriğine bakar — aynı kaynak (örn. TechCrunch) hem
yapay zeka hem telefon hem sosyal medya haberi yayınlayabildiği için
kategori artık Source değil Article bazında hesaplanıyor.
"""

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


def classify_slug(title, summary):
    """Başlık + özet metnine göre en iyi eşleşen kategori slug'ını döndürür."""
    text = f'{title} {summary}'.lower()

    best_slug = FALLBACK_SLUG
    best_score = 0
    for slug, (_, keywords) in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > best_score:
            best_score = score
            best_slug = slug

    return best_slug


def all_categories():
    """(slug, isim) çiftlerini, fallback dahil, sırayla döndürür."""
    for slug, (name, _) in TOPIC_KEYWORDS.items():
        yield slug, name
    yield FALLBACK_SLUG, FALLBACK_NAME
