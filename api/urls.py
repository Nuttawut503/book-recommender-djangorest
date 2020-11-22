from django.urls import path
from api import views

urlpatterns = [
    path('search', views.search_books),
    path('book', views.more_book_info),
]
