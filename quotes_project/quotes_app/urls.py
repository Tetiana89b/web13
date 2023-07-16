from django.urls import path

from . import views

app_name = 'quotes_app'

urlpatterns = [
    path('', views.base, name='base'),
    path('author_list/', views.author_list, name='author_list'),
    path('quote_list/<int:author_id>/', views.quote_list, name='quote_list'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_q/', views.add_quote, name='add_quote'),
    path('authors/<int:pk>/', views.author_detail, name='author_detail'),
    path('quotes/tag/<str:tag_name>/',
         views.quote_list_by_tag, name='quote_list_by_tag'),
    path('quote_list/', views.quote_list, name='quote_list'),
]
