from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from .customExceptions import ProductOutOfStock
from .serializers import *

# Create your views here.
def hello(request):
    data = Product.objects.all()
    if data:
        print("before update" , data[0].name)
        data[0].name = "ABC"
        data[0].save()
        print("saved successfully")
        data[0].refresh_from_db()
        #data= Product.objects.all()
        print("After update", data[0].name)
        print(data[0].name)
        return HttpResponse('Hello World')

@api_view(['GET'])
def get_products(request):
    data = Product.objects.all()
    serializedProducts = ProductSerializer(data,many=True)
    return Response(serializedProducts.data)

@api_view(['GET'])
def get_product(request,id):
    try:
        data = Product.objects.filter(id=id).first()
        #data = Product.objects.get(id=id)
        #print(data)
        if not data:
            raise ProductOutOfStock("Product Not Found")
        serialized_product = ProductSerializer(data)
        return Response(serialized_product.data)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except ProductOutOfStock:
        return Response(status=status.HTTP_404_NOT_FOUND,data="Oops, Sorry! Product Out of Stock!")
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_product(request):
    try:
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status = status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_product(request,id):
    try:
        data = Product.objects.get(id=id)
        data.delete()
        return Response(status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def filter_products(request):
    name = request.GET.get('name')
    description = request.GET.get('description')
    price = request.GET.get('price')
    is_available = request.GET.get('is_available')
    #min_price = request.GET.get('min_price')
    #max_price = request.GET.get('max_price')
    logic = request.GET.get('logic')

    products = Product.objects.all()

    if logic == 'or':
        combined_filter = Q()

        if name:
            combined_filter |= Q(name__icontains = name)
        if description:
            combined_filter |= Q(description__icontains = description)
        if is_available:
            combined_filter |= Q(is_available = is_available)
        if price:
            for p in price.split(','):
                combined_filter |= Q(price = p)

        products = products.filter(combined_filter)

    else:
        if name:
            products = products.filter(name__icontains = name)
        if description:
            products = products.filter(description__icontains = description)
        if is_available:
            products = products.filter(is_available = is_available)
        if price:
            price_filter = Q()
            for p in price.split(','):
                price_filter |= Q(price = p)
            products = products.filter(price_filter) 

    #if min_price and max_price:
        #products = products.filter(price__gte = min_price, price__lte = max_price)

    #if min_price:
        #products = products.filter(price__gte = min_price)

    #if max_price:
        #products = products.filter(price__lte = max_price) 


    serialized_products = ProductSerializer(products, many = True)
    return Response(serialized_products.data)