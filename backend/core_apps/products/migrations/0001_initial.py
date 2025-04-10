# Generated by Django 5.0.2 on 2025-03-16 19:57

import autoslug.fields
import core_apps.products.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import taggit.managers
import uuid
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="name", unique=True
                    ),
                ),
                ("description", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="products.productcategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Category",
                "verbose_name_plural": "Product Categories",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="name", unique=True
                    ),
                ),
                ("description", models.TextField()),
                ("short_description", models.CharField(max_length=255)),
                ("deal_url", models.URLField(max_length=1000)),
                ("shorten_url", models.URLField(blank=True, max_length=255)),
                (
                    "url_shortening_status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("price", models.CharField(max_length=50)),
                ("compare_at_price", models.CharField(blank=True, max_length=50)),
                ("coupon", models.CharField(blank=True, max_length=255)),
                ("is_coupon", models.BooleanField(default=False)),
                ("stock_quantity", models.PositiveIntegerField(default=1)),
                ("sku", models.CharField(blank=True, max_length=100, unique=True)),
                ("vendor", models.CharField(max_length=50)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("active", "Active"),
                            ("inactive", "Inactive"),
                            ("out_of_stock", "Out of Stock"),
                            ("archived", "Archived"),
                        ],
                        default="draft",
                        max_length=20,
                    ),
                ),
                ("start_date", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "end_date",
                    models.DateTimeField(
                        default=core_apps.products.models.get_default_end_date
                    ),
                ),
                ("views_count", models.PositiveIntegerField(default=0)),
                ("sales_count", models.PositiveIntegerField(default=0)),
                ("is_featured", models.BooleanField(default=False)),
                ("is_new", models.BooleanField(default=True)),
                (
                    "weight",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                    ),
                ),
                ("dimensions", models.CharField(blank=True, max_length=100)),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_creator",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="products.productcategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
                "ordering": ["-created_at"],
                "permissions": [
                    ("can_create_product", "Can create product"),
                    ("can_edit_product", "Can edit product"),
                    ("can_delete_product", "Can delete product"),
                ],
                "default_permissions": ["view"],
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image_url", models.CharField(max_length=255)),
                ("is_primary", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="products.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Image",
                "verbose_name_plural": "Product Images",
                "ordering": ["-is_primary", "-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["name"], name="products_pr_name_9ff0a3_idx"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["slug"], name="products_pr_slug_3edc0c_idx"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["sku"], name="products_pr_sku_ca0cdc_idx"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["status"], name="products_pr_status_041708_idx"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(
                fields=["created_at"], name="products_pr_created_52f0d7_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(
                fields=["start_date"], name="products_pr_start_d_4a6479_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(
                fields=["end_date"], name="products_pr_end_dat_5ed2d7_idx"
            ),
        ),
    ]
