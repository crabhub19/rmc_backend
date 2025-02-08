from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']  # Include all fields you want to serialize
        

class BrandSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Brand
        fields = ['id', 'name', 'image', 'image_url']  # Include all fields you want to serialize
        
    def get_image_url(self, obj):
        return obj.image.url

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','name','image','price','slug','image_url']

    def get_image_url(self, obj):
        return obj.image.url

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Nested serializer for Category
    brand = BrandSerializer(read_only=True)  # Nested serializer for Brand
    image_url = serializers.SerializerMethodField()
    similar_products = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'brand', 'details', 'price', 'image', 'slug','image_url', 'similar_products'
        ]
    def get_image_url(self, obj):
        return obj.image.url
    def get_similar_products(self, obj):
        products = Product.objects.filter(category=obj.category).exclude(pk=obj.pk)[:4]
        serializer = ProductSerializer(products, many=True)
        return serializer.data
