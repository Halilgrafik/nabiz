from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(max_length=100)
    feed_url = models.URLField(unique=True)
    website_url = models.URLField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='articles')
    title = models.CharField(max_length=500)
    link = models.URLField(unique=True)
    guid = models.CharField(max_length=500, blank=True, db_index=True)
    summary = models.TextField(blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at', '-fetched_at']

    def __str__(self):
        return self.title


class ReadEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='read_events')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='read_events')
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-read_at']

    def __str__(self):
        return f'{self.user} -> {self.article}'
