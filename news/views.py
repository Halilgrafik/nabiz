import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Article, Category, ReadEvent


def article_list(request):
    articles = Article.objects.select_related('source', 'category')

    category_slug = request.GET.get('category')
    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        articles = articles.filter(category=active_category)

    active_lang = request.GET.get('lang')
    if active_lang not in ('tr', 'en'):
        active_lang = None
    else:
        articles = articles.filter(source__language=active_lang)

    paginator = Paginator(articles, 30)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'active_category': active_category,
        'active_lang': active_lang,
    }
    return render(request, 'news/article_list.html', context)


def read_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user.is_authenticated:
        ReadEvent.objects.create(user=request.user, article=article)
    return redirect(article.link)


@login_required
def dashboard(request):
    events = ReadEvent.objects.filter(user=request.user)
    today = timezone.localdate()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    total_read = events.count()
    read_this_week = events.filter(read_at__date__gte=week_ago).count()
    read_this_month = events.filter(read_at__date__gte=month_ago).count()

    category_breakdown = (
        events.values('article__category__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    streak = _reading_streak(events, today)

    last_14_days = _daily_counts(events, today, days=14)

    context = {
        'total_read': total_read,
        'read_this_week': read_this_week,
        'read_this_month': read_this_month,
        'category_breakdown': category_breakdown,
        'streak': streak,
        'chart_labels': json.dumps([d.strftime('%d.%m') for d, _ in last_14_days]),
        'chart_values': json.dumps([c for _, c in last_14_days]),
    }
    return render(request, 'news/dashboard.html', context)


def _reading_streak(events, today):
    read_dates = set(events.values_list('read_at__date', flat=True))
    streak = 0
    day = today
    while day in read_dates:
        streak += 1
        day -= timedelta(days=1)
    return streak


def _daily_counts(events, today, days):
    counts_by_date = dict(
        events.filter(read_at__date__gte=today - timedelta(days=days - 1))
        .values('read_at__date')
        .annotate(count=Count('id'))
        .values_list('read_at__date', 'count')
    )
    result = []
    for i in range(days - 1, -1, -1):
        day = today - timedelta(days=i)
        result.append((day, counts_by_date.get(day, 0)))
    return result
