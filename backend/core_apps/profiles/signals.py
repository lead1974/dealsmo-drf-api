import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from core_apps.profiles.models import Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, username=instance.email)
        logger.info(f"{instance}'s profile has been created.")
    else:
        instance.profile.save()
