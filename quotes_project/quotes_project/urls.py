from django.contrib import admin
from django.urls import include, path
from quotes_app import views

urlpatterns = [
    path('', views.base, name='base'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('quotes_app', include('quotes_app.urls')),
]
