from rest_framework import serializers
from .models import Product, ProductImage, ProductCategory


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'is_primary']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    main_image = serializers.CharField(read_only=True)
    gallery = serializers.ListField(read_only=True)
    is_published = serializers.BooleanField(read_only=True)
    has_discount = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    has_deal = serializers.BooleanField(read_only=True)
    current_price = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'deal_url', 'shorten_url', 'url_shortening_status',
            'price', 'compare_at_price',
            'deal_start_date', 'deal_end_date',
            'stock_quantity', 'sku',
            'images', 'main_image', 'gallery',
            'category', 'tags',
            'vendor',
            'status', 'start_date', 'end_date',
            'views_count', 'sales_count',
            'is_featured', 'is_new',
            'weight', 'dimensions',
            'is_published', 'has_discount', 'discount_percentage',
            'has_deal', 'current_price',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'slug', 'sku', 'shorten_url', 'url_shortening_status',
            'views_count', 'sales_count', 'created_at', 'updated_at'
        ] 