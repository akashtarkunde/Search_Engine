from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Product
from django.db.models import Q
from .serializers import ProductSerializer
from rest_framework.response import Response
from fastapi import FastAPI, HTTPException
import requests
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
def upload_products(request):
    # This view can send data to FastAPI
    products = request.data
    print(products)
    fastapi_url = "http://localhost:8002/upload-products/"  # Adjust port if needed
    response = requests.post(fastapi_url, json=products)

    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({"error": response.text}, status=response.status_code)
@api_view(['GET'])
def search_products(request):
    query = request.GET.get('q', '')
    brand = request.GET.get('brand', '')
    size = request.GET.get('size', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    query_words = query.split()  # Split the query into individual words
    print(f"Search query: {query_words}")  # Debugging log

    # Construct the search query with multiple words
    search_query = Q()
    for word in query_words:
        word_query = Q(ProductName__icontains=word) | \
                     Q(BrandName__icontains=word) | \
                     Q(BrandDesc__icontains=word) | \
                     Q(ProductSize__icontains=word) | \
                     Q(Currency__icontains=word) | \
                     Q(Category__icontains=word)
        search_query &= word_query  # Combine the queries to require all words to be present

    # Apply column filters
    if brand:
        search_query &= Q(BrandName__icontains=brand)
    if size:
        search_query &= Q(ProductSize__icontains=size)
    if category:
        search_query &= Q(Category__icontains=category)
    if min_price:
        search_query &= Q(SellPrice__gte=min_price)
    if max_price:
        search_query &= Q(SellPrice__lte=max_price)

    products = Product.objects.filter(search_query)

    # Serialize the results
    serializer = ProductSerializer(products, many=True)

    # Debugging logs
    #print(f"Raw Results: {[{'ProductName': p.ProductName, 'MRP': p.MRP, 'SellPrice': p.SellPrice} for p in products]}")
    #print(f"Serialized Results: {serializer.data}")

    #return Response(serializer.data)

    # Send results to FastAPI
    fastapi_url = "http://localhost:8002/upload-products/"
    print("sending to fast api")
    response = requests.post(fastapi_url, json=serializer.data)

    # Handle FastAPI response
    if response.status_code == 200:
        print("Response received from FastAPI")
        print("FastAPI Response:", response.json())
        return Response(serializer.data)
    else:
        print("response failed")
        return Response({"error": response.text}, status=response.status_code)

def search_page(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(ProductName__icontains=query)
    else:
        products = Product.objects.all()

    context = {
        'products': products,
    }
    return render(request, 'akash_search_app/search.html', context)
