from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('accounts/register/', core_views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('news.urls')),
]
