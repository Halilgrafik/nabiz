from datetime import datetime, timezone as dt_timezone

import feedparser
import requests
from django.core.management.base import BaseCommand

from news.categorize import all_categories, classify_slug
from news.models import Article, Category, Source


class Command(BaseCommand):
    help = 'Aktif kaynaklardaki RSS feed\'lerini çekip yeni haberleri kaydeder.'

    def handle(self, *args, **options):
        self._categories = {}
        for slug, name in all_categories():
            category, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name})
            self._categories[slug] = category

        total_new = 0
        total_skipped = 0

        for source in Source.objects.filter(is_active=True):
            try:
                new_count, skipped_count = self._fetch_source(source)
                total_new += new_count
                total_skipped += skipped_count
                self.stdout.write(f'{source.name}: {new_count} yeni, {skipped_count} atlandı')
            except Exception as exc:
                self.stderr.write(f'{source.name}: HATA — {exc}')

        self.stdout.write(self.style.SUCCESS(f'Toplam: {total_new} yeni, {total_skipped} atlandı'))

    def _fetch_source(self, source):
        response = requests.get(source.feed_url, timeout=30, headers={'User-Agent': 'Nabiz/1.0'})
        response.raise_for_status()
        feed = feedparser.parse(response.content)

        new_count = 0
        skipped_count = 0

        for entry in feed.entries:
            link = entry.get('link', '')
            guid = entry.get('id', '') or link
            if not link:
                continue

            if Article.objects.filter(link=link).exists() or (guid and Article.objects.filter(guid=guid).exists()):
                skipped_count += 1
                continue

            title = entry.get('title', '')[:500]
            summary = entry.get('summary', '')
            category = self._categories[classify_slug(title, summary)]

            Article.objects.create(
                source=source,
                category=category,
                title=title,
                link=link,
                guid=guid[:500],
                summary=summary,
                published_at=self._parse_date(entry),
            )
            new_count += 1

        return new_count, skipped_count

    @staticmethod
    def _parse_date(entry):
        parsed = entry.get('published_parsed') or entry.get('updated_parsed')
        if not parsed:
            return None
        return datetime(*parsed[:6], tzinfo=dt_timezone.utc)
