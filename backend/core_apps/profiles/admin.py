from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'username', 'first_name', 'last_name', 'phone_number', 'country', 'city']
    fields = ['username', 'first_name', 'last_name', 'user', 'phone_number', 'about_me', 'gender', 'country', 'city', 'profile_photo', 'twitter_handle', 'followers']


admin.site.register(Profile, ProfileAdmin)