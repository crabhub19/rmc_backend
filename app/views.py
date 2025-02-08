from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .pagination import *
from .models import *
from .serializers import *
# Create your views here.

class ProductList(ListAPIView):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    pagination_class = TenNumberPagination
    permission_classes = [AllowAny]
    
@api_view(['GET'])
@permission_classes([AllowAny])
def ProductDetail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)