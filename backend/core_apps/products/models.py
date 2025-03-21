from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from django.utils import timezone
from datetime import timedelta
from core_apps.common.models import TimeStampedModel
from django.core.validators import MinValueValidator
from decimal import Decimal
import random

User = get_user_model()


def get_default_end_date():
    return timezone.now() + timedelta(days=365*50)


class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image_url = models.CharField(max_length=255)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ["-is_primary", "-created_at"]

    def __str__(self):
        return f"Image URL: {self.image_url}"


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    # Basic Information Fields
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=255)

    # URL Fields
    deal_url = models.URLField(max_length=1000)
    shorten_url = models.URLField(max_length=255, blank=True)
    url_shortening_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )

    # Pricing Fields
    price = models.CharField(max_length=50)
    compare_at_price = models.CharField(max_length=50, blank=True)
    coupon = models.CharField(max_length=255, blank=True)
    is_coupon = models.BooleanField(default=False)

    # Stock Management Fields
    stock_quantity = models.PositiveIntegerField(default=1)
    sku = models.CharField(max_length=100, unique=True, blank=True)

    # Categorization Fields
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, related_name='products')
    tags = TaggableManager()

    # Vendor Information
    vendor = models.CharField(max_length=50)

    # Author Information
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_creator')

    # Status and Visibility Fields
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('out_of_stock', 'Out of Stock'),
            ('archived', 'Archived'),
        ],
        default='draft'
    )
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=get_default_end_date)

    # Statistics Fields
    views_count = models.PositiveIntegerField(default=0)
    sales_count = models.PositiveIntegerField(default=0)

    # Additional Fields
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        null=True,
        blank=True
    )
    dimensions = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
            models.Index(fields=['sku']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
        ]
        permissions = [
            ("can_create_product", "Can create product"),
            ("can_edit_product", "Can edit product"),
            ("can_delete_product", "Can delete product"),
        ]
        default_permissions = ['view']  # This ensures only view permission is granted by default

    def __str__(self):
        return self.name

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be after start date")

    def save(self, *args, **kwargs):
        if not self.sku:
            # Generate SKU based on category and timestamp
            prefix = self.category.slug[:3].upper() if self.category else 'PRD'
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            base_sku = f"{prefix}-{timestamp}-{random_suffix}"
            
            # Ensure SKU uniqueness
            counter = 1
            sku = base_sku
            while Product.objects.filter(sku=sku).exists():
                sku = f"{base_sku}-{counter}"
                counter += 1
            
            self.sku = sku
        
        # Set author if not set and user is authenticated
        if not self.author and hasattr(self, '_current_user') and self._current_user.is_authenticated:
            self.author = self._current_user
            
        super().save(*args, **kwargs)

    @property
    def main_image(self):
        """Returns the primary image URL or the first image URL if no primary image exists"""
        primary_image = self.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.image_url
        first_image = self.images.first()
        return first_image.image_url if first_image else None

    @property
    def gallery(self):
        """Returns all image URLs except the primary image"""
        return [img.image_url for img in self.images.filter(is_primary=False)]

    @property
    def is_published(self):
        now = timezone.now()
        return (
            self.status == 'active' and
            self.start_date <= now <= self.end_date and
            self.stock_quantity > 0
        )

    @property
    def has_discount(self):
        return bool(self.compare_at_price and self.compare_at_price != self.price)

    @property
    def discount_percentage(self):
        if not self.has_discount:
            return 0
        try:
            original_price = float(self.compare_at_price)
            current_price = float(self.price)
            return int(((original_price - current_price) / original_price) * 100)
        except (ValueError, ZeroDivisionError):
            return 0

    @property
    def has_deal(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    @property
    def current_price(self):
        if self.has_deal:
            return self.price
        return self.compare_at_price if self.compare_at_price else self.price

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def increment_sales(self):
        self.sales_count += 1
        self.stock_quantity = max(0, self.stock_quantity - 1)
        if self.stock_quantity == 0:
            self.status = 'out_of_stock'
        self.save(update_fields=['sales_count', 'stock_quantity', 'status'])