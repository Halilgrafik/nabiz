from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import include, path
from django.views.generic import TemplateView

from core import views as core_views
from core.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('accounts/login/', LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('accounts/register/', core_views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('news.urls')),
]
