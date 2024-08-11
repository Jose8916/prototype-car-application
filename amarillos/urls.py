"""amarillos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, logout_then_login
from django.contrib.sitemaps.views import sitemap
from apps.users.views import login_user
admin.autodiscover()
admin.site.enable_nav_sidebar = False
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/login/', LoginView.as_view(template_name="users/login.html"), name="login"),
    # path('accounts/logout', logout_then_login, name="logout"),
    path(r'', login_user, name='login'),
    path('', include(('apps.users.urls', 'users'), namespace="users")),
    path('', include(('apps.taxes.urls', 'taxes'), namespace="taxes")),
    path('', include(('apps.regions.urls', 'regions'), namespace="regions")),
    path('', include(('apps.vehicles.urls', 'vehicles'), namespace="vehicles")),
    path('', include(('apps.services.urls', 'services'), namespace="services")),
    path('', include(('apps.guests.urls', 'guests'), namespace="guests")),
    #path('sitemap.xml',sitemap,{'sitemaps': sitemaps.sitemaps},name='django.contrib.sitemaps.views.sitemap',),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
