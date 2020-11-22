from django.urls import path
from api import views

urlpatterns = [
    path('search', views.search_books),
    path('book', views.more_book_info),
    path('predict', views.predict_books),
    path('review', views.list_of_books),
]
