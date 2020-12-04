from django.conf.urls import url
from . import views

app_name = "categories"

urlpatterns = [
    url(r'^$',views.ListCategory.as_view(), name='all'),
    url(r'^new/$', views.CreateCategory.as_view(), name='create'),
    url(r'^posts/in/(?P<slug>[-\w]+)/', views.SingleCategory.as_view(), name='single'),
    url(r'join/(?P<slug>[-\w]+)/$', views.JoinCategory.as_view(),name='join'),
    url(r'leave/(?P<slug>[-\w]+)/$',views.LeaveCategory.as_view(), name='leave')
]
