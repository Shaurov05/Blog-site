"""my_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings
from posts.views import UserPosts

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^$', views.ListCategory2.as_view(), name='index_page'),

    url(r'^categories/', include("categories.urls",namespace="categories")),
    url(r"^accounts/", include("accounts.urls", namespace="accounts")),
    url(r"^posts/", include("posts.urls", namespace="posts")),

    url(r"^test/$", views.TestPage.as_view(), name='test'),
    url(r"^thanks/$", views.ThanksPage.as_view(), name='thanks'),
    url(r"by/(?P<username>[-\w]+)/$", UserPosts.as_view(),name="for_user"),
    # url(r"^profile/$", views.ProfileView.as_view(), name='profile'),

    path('national_news/', views.national_news, name='national'),
    path('sports/',views.sports_news, name='sports'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
    url(r'^__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
