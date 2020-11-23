from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import pandas as pd
books_csv = pd.read_csv('/root/djangorest/api/books_cut.csv')
ratings_csv = pd.read_csv('/root/djangorest/api/ratings_cut.csv')
corrs_csv = pd.read_csv('/root/djangorest/api/corrs_cut.csv')

def to_json(filtered_books, ratings_included=False):
    json = []
    for i in filtered_books.index:
        book = {
            'id': str(filtered_books.id[i]),
            'title': str(filtered_books.title[i]),
            'author': str(filtered_books.authors[i]),
            'img_url': str(filtered_books.image_url[i]),
            'avg_score': float(filtered_books.average_rating[i]),
        }
        if ratings_included:
            book['counting_scores'] = [
                int(filtered_books['ratings_1'][i]),
                int(filtered_books['ratings_2'][i]),
                int(filtered_books['ratings_3'][i]),
                int(filtered_books['ratings_4'][i]),
                int(filtered_books['ratings_5'][i]),
            ]
        json.append(book)
    return json

# Create your views here.

@api_view(['POST'])
def search_books(request):
    query = str(request.data.get('query'))
    columns = ['title', 'authors']
    results = books_csv[books_csv[columns].apply(lambda column: column.str.contains(query, case=False)).any(axis=1)]
    return Response(to_json(results))

@api_view(['POST'])
def more_book_info(request):
    book_id = int(request.data.get('book_id'))
    results = books_csv[books_csv.id == book_id]
    return Response(to_json(results, ratings_included=True))

@api_view(['POST'])
def predict_books(request):
    rating_book = json.loads(request.data.get('rating_books'))
    my_rating = pd.Series(map(float, rating_book.values()), index=map(int, rating_book.keys()))
    candidates = pd.Series()
    for i in my_rating.index:
        similarities = corrs_csv[str(i)].dropna()
        similarities = similarities.map(lambda x: x * my_rating[i])
        candidates = candidates.append(similarities)
    candidates = candidates.groupby(candidates.index).sum()
    candidates.sort_values(inplace = True, ascending = False)
    candidates = candidates.drop([*filter(lambda x: x in candidates.index, my_rating.index)])[:10]
    results = books_csv[books_csv.id.isin(candidates.index)]
    return Response(to_json(results))

@api_view(['POST'])
def list_of_books(request):
    id_list = json.loads(request.data.get('id_list'))
    results = books_csv[books_csv.id.isin([*map(int, id_list)])]
    return Response(to_json(results))
