from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
books = pd.read_csv('/root/djangorest/api/books.csv')

def to_full_detail_book(filtered_books):
    columns_name = [*books.keys()]
    models = []
    for i in range(len(filtered_books)):
        models.append({
            'id': str(books.id[i]),
            'title': str(books.title[i]),
            'author': str(books.authors[i]),
            'img_url': str(books.image_url[i]),
            'avg_score': float(books.average_rating[i]),
            'counting_scores': [
                int(books['ratings_1'][i]),
                int(books['ratings_2'][i]),
                int(books['ratings_3'][i]),
                int(books['ratings_4'][i]),
                int(books['ratings_5'][i]),
            ], 
        })
    return models

def to_minimal_detail_book(filtered_books):
    columns_name = [*books.keys()]
    models = []
    for i in range(len(filtered_books)):
        models.append({
            'id': str(books.id[i]),
            'title': str(books.title[i]),
            'author': str(books.authors[i]),
            'imgUrl': str(books.image_url[i]),
            'avgScore': float(books.average_rating[i]),
        })
    return models

# Create your views here.

@api_view(['POST'])
def search_books(request):
    query = str(request.data.get('query'))
    results = books[books[['title', 'authors']].apply(lambda x: x.str.contains(query, case=False)).any(axis=1)]
    return Response(to_minimal_detail_book(results))

