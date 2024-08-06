from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Product
from django.db.models import Q
from .serializers import ProductSerializer
from rest_framework.response import Response


@api_view(['GET'])
def search_products(request):
    query = request.GET.get('q', '')
    print(f"Search query: {query}")  # Debugging log

    if query:
        search_query = Q(ProductName__icontains=query) | \
                       Q(BrandName__icontains=query) | \
                       Q(BrandDesc__icontains=query) | \
                       Q(ProductSize__icontains=query) | \
                       Q(Currency__icontains=query) | \
                       Q(MRP__icontains=query) | \
                       Q(SellPrice__icontains=query) | \
                       Q(Discount__icontains=query) | \
                       Q(Category__icontains=query)
        products = Product.objects.filter(search_query)
    else:
        products = Product.objects.all()

    results = []
    for product in products:
        result = {
            'ProductName': product.ProductName,
            'BrandName': product.BrandName,
            'BrandDesc': product.BrandDesc,
            'ProductSize': product.ProductSize,
            'Currency': product.Currency,
            'MRP': product.MRP,
            'SellPrice': product.SellPrice,
            'Discount': product.Discount,
            'Category': product.Category,
        }
        results.append(result)

    #print(f"Results: {results}")  # Debugging log

    serializer = ProductSerializer(products, many=True)
    # Print out raw data before serialization for debugging
    print(f"Raw Results: {[{'ProductName': p.ProductName, 'MRP': p.MRP, 'SellPrice': p.SellPrice} for p in products]}")

    print(f"Serialized Results: {serializer.data}")  # Debugging log

    return Response(serializer.data)


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
