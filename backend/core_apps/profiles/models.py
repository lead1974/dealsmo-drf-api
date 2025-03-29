from django.contrib.auth import get_user_model
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from core_apps.common.models import TimeStampedModel
from django.db.models import Avg
from core_apps.articles.models import Article

User = get_user_model()


class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = (
            "M",
            _("Male"),
        )

        FEMALE = (
            "F",
            _("Female"),
        )
        OTHER = (
            "O",
            _("Other"),
        )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(max_length=255, unique=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    phone_number = PhoneNumberField(
        verbose_name=_("phone number"), max_length=30, blank=True, null=True
    )
    about_me = models.TextField(
        verbose_name=_("about me"), default="say something about yourself"
    )
    gender = models.CharField(
        verbose_name=_("gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=20,
    )
    country = CountryField(
        verbose_name=_("country"), default="USA", blank=False, null=False
    )
    city = models.CharField(
        verbose_name=_("city"),
        max_length=180,
        default="Los Angeles",
        blank=False,
        null=False,
    )
    avatar = CloudinaryField(verbose_name=_("Avatar"), blank=True, null=True)

    twitter_handle = models.CharField(
        verbose_name=_("twitter handle"), max_length=20, blank=True
    )
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", blank=True
    )

    report_count = models.IntegerField(verbose_name=_("Report Count"), default=0)
    reputation = models.IntegerField(verbose_name=_("Reputation"), default=100)

    def __str__(self) -> str:
        return f"{self.user.first_name}'s Profile"

    @property
    def is_banned(self) -> bool:
        return self.report_count >= 5

    def update_reputation(self):
        self.reputation = max(0, 100 - self.report_count * 10)

    def __str__(self):
        return f"{self.user.email}'s Profile"

    def follow(self, profile):
        self.followers.add(profile)

    def unfollow(self, profile):
        self.followers.remove(profile)

    def check_following(self, profile):
        return self.followers.filter(pkid=profile.pkid).exists()
    
    def get_average_rating(self):
        # Get all articles authored by this user
        user_articles = Article.objects.filter(author=self.user)
        
        # Calculate average rating across all articles
        average = user_articles.aggregate(Avg('ratings__rating'))['ratings__rating__avg']
        return average if average is not None else 0.0
    
    @property
    def is_banned(self) -> bool:
        return self.report_count >= 5
