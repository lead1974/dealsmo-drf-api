from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from .models import Product
from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


@shared_task
def shorten_product_url(product_id):
    """
    Celery task to shorten the product URL
    """
    try:
        product = Product.objects.get(id=product_id)
        # TODO: Implement URL shortening logic here
        # For now, we'll just mark it as completed
        product.shorten_url = product.deal_url
        product.url_shortening_status = 'completed'
        product.save(update_fields=['shorten_url', 'url_shortening_status'])
    except Product.DoesNotExist:
        pass


@receiver(post_save, sender=Product)
def trigger_url_shortening(sender, instance, created, **kwargs):
    """
    Signal handler to trigger URL shortening when a product is created
    or when the deal_url is updated
    """
    if created or instance.tracker.has_changed('deal_url'):
        instance.url_shortening_status = 'pending'
        instance.save(update_fields=['url_shortening_status'])
        shorten_product_url.delay(instance.id)


@receiver(post_save, sender=User)
def assign_product_permissions(sender, instance, created, **kwargs):
    """
    Signal to automatically assign product permissions to authenticated users
    """
    if created and instance.is_authenticated:
        content_type = ContentType.objects.get_for_model(Product)
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=['can_create_product', 'can_edit_product', 'can_delete_product']
        )
        instance.user_permissions.add(*permissions) 