from django.contrib import admin
from django.urls import path, include
from search import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing),
    path('search/', include('search.urls')),
    path('accounts/', include('accounts.urls')),
]
