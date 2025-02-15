import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from config.settings.base import AUTH_USER_MODEL
from core_apps.profiles.models import Profile
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

User = get_user_model()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            username=instance.username or instance.email
        )
    else:
        instance.profile.save()