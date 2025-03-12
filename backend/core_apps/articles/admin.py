from django.contrib import admin

from . import models


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ["pkid", "name", "slug", "parent"]
    list_display_links = ["pkid", "name"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["name", "description"]
    ordering = ["name"]


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["pkid", "author", "title", "slug", "view_count"]
    list_display_links = ["pkid", "author"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["title", "body", "tags"]
    ordering = ["-created_at"]


class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ["pkid", "article", "user", "viewer_ip"]
    list_display_links = ["pkid", "user"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["article", "user", "viewer_ip"]


class ClapAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "user", "article"]
    list_display_links = ["pkid", "user"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["user", "article"]


admin.site.register(models.ArticleCategory, ArticleCategoryAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleView, ArticleViewAdmin)
admin.site.register(models.Clap, ClapAdmin)
