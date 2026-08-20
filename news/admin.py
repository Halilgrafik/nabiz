from django.contrib import admin

from .models import Article, Category, ReadEvent, Source


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'feed_url')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'feed_url')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'category', 'published_at', 'fetched_at')
    list_filter = ('category', 'source')
    search_fields = ('title', 'summary')
    date_hierarchy = 'published_at'


@admin.register(ReadEvent)
class ReadEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'read_at')
    list_filter = ('user',)
