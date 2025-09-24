from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.post_list, name='post_list'),
    path('about/', views.about, name='about'),
    path("accounts/", include("accounts.urls")),
]