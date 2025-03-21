from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductImage, ProductCategory


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image_url', 'is_primary', 'preview_image']
    readonly_fields = ['preview_image']

    def preview_image(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image_url)
        return "-"
    preview_image.short_description = 'Preview'


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'created_at']
    list_filter = ['parent', 'created_at']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'sku', 'price', 'compare_at_price', 'stock_quantity',
        'status', 'vendor', 'author', 'is_featured', 'is_new',
        'created_at', 'views_count', 'sales_count'
    ]
    list_filter = [
        'status', 'vendor', 'author', 'is_featured', 'is_new',
        'category', 'created_at', 'start_date', 'end_date', 'is_coupon'
    ]
    search_fields = [
        'name', 'sku', 'description', 'short_description',
        'deal_url', 'shorten_url', 'vendor', 'coupon'
    ]
    readonly_fields = [
        'slug', 'sku', 'shorten_url', 'url_shortening_status',
        'views_count', 'sales_count', 'created_at', 'updated_at',
        'main_image', 'gallery', 'is_published', 'has_discount',
        'discount_percentage', 'has_deal', 'current_price'
    ]
    inlines = [ProductImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'short_description')
        }),
        ('URLs', {
            'fields': ('deal_url', 'shorten_url', 'url_shortening_status')
        }),
        ('Pricing', {
            'fields': ('price', 'compare_at_price', 'coupon', 'is_coupon')
        }),
        ('Stock Management', {
            'fields': ('stock_quantity', 'sku')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Vendor Information', {
            'fields': ('vendor',)
        }),
        ('Author Information', {
            'fields': ('author',)
        }),
        ('Status and Visibility', {
            'fields': ('status', 'start_date', 'end_date')
        }),
        ('Statistics', {
            'fields': ('views_count', 'sales_count')
        }),
        ('Additional Fields', {
            'fields': ('is_featured', 'is_new', 'weight', 'dimensions')
        }),
        ('Computed Fields', {
            'fields': ('main_image', 'gallery', 'is_published', 'has_discount',
                      'discount_percentage', 'has_deal', 'current_price'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    actions = ['mark_as_featured', 'mark_as_not_featured', 'mark_as_new', 'mark_as_not_new']

    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_as_featured.short_description = "Mark selected products as featured"

    def mark_as_not_featured(self, request, queryset):
        queryset.update(is_featured=False)
    mark_as_not_featured.short_description = "Mark selected products as not featured"

    def mark_as_new(self, request, queryset):
        queryset.update(is_new=True)
    mark_as_new.short_description = "Mark selected products as new"

    def mark_as_not_new(self, request, queryset):
        queryset.update(is_new=False)
    mark_as_not_new.short_description = "Mark selected products as not new"
