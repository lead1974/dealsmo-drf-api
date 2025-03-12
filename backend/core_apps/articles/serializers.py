from rest_framework import serializers

from core_apps.article_responses.serializers import ArticleResponseSerializer
from core_apps.articles.models import Article, ArticleView, Clap, ArticleCategory
from core_apps.article_bookmarks.models import Bookmark
from core_apps.article_bookmarks.serializers import BookmarkSerializer
from core_apps.profiles.serializers import ProfileSerializer


class TagListField(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, list):
            return value
        return [tag.name for tag in value.all()]

    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise serializers.ValidationError("Expected a list of tags")

        tag_objects = []
        for tag_name in data:
            tag_name = tag_name.strip()

            if not tag_name:
                continue
            tag_objects.append(tag_name)
        return tag_objects


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ["pkid", "id", "name", "slug", "description", "parent", "created_at", "updated_at"]


class ArticleSerializer(serializers.ModelSerializer):
    author_info = ProfileSerializer(source="author.profile", read_only=True)
    banner_image = serializers.SerializerMethodField()
    estimated_reading_time = serializers.ReadOnlyField()
    tags = TagListField()
    views = serializers.SerializerMethodField()
    average_rating = serializers.ReadOnlyField()
    bookmarks = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    claps_count = serializers.SerializerMethodField()
    article_responses = ArticleResponseSerializer(many=True, read_only=True)
    article_responses_count = serializers.IntegerField(
        source="article_responses.count", read_only=True
    )
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    category = ArticleCategorySerializer(read_only=True)
    category_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    status = serializers.ChoiceField(choices=Article.Status.choices, required=False)
    is_published = serializers.ReadOnlyField()
    start_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    end_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")

    def validate_status(self, value):
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError("Authentication required to change status")

        # If this is an update operation
        if self.instance:
            # Only author or staff can change status
            if not (request.user.is_staff or request.user == self.instance.author):
                raise serializers.ValidationError("Only the author or staff can change the article status")

        return value

    def validate(self, data):
        if 'start_date' in data and 'end_date' in data:
            if data['start_date'] >= data['end_date']:
                raise serializers.ValidationError({
                    'end_date': 'End date must be after start date'
                })
        elif 'start_date' in data and self.instance:
            if data['start_date'] >= self.instance.end_date:
                raise serializers.ValidationError({
                    'start_date': 'Start date must be before end date'
                })
        elif 'end_date' in data and self.instance:
            if self.instance.start_date >= data['end_date']:
                raise serializers.ValidationError({
                    'end_date': 'End date must be after start date'
                })
        return data

    def get_article_responses_count(self, obj):
        return obj.article_responses.count()

    def get_claps_count(self, obj):
        return obj.claps.count()

    def get_bookmarks(self, obj):
        bookmarks = Bookmark.objects.filter(article=obj)
        return BookmarkSerializer(bookmarks, many=True).data

    def get_bookmarks_count(self, obj):
        return Bookmark.objects.filter(article=obj).count()

    def get_average_rating(self, obj):
        return obj.average_rating()

    def get_views(self, obj):
        return ArticleView.objects.filter(article=obj).count()

    def get_banner_image(self, obj):
        if obj.banner_image:
            return obj.banner_image.url
        return None

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%dT%H:%M:%SZ")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ")

    def create(self, validated_data):
        category_id = validated_data.pop("category_id", None)
        article = super().create(validated_data)
        
        if category_id:
            try:
                category = ArticleCategory.objects.get(id=category_id)
                article.category = category
                article.save()
            except ArticleCategory.DoesNotExist:
                pass
                
        return article

    def update(self, instance, validated_data):
        print("Update method called with data:", validated_data)
        category_id = validated_data.pop("category_id", None)
        print("Category ID from request:", category_id)
        article = super().update(instance, validated_data)
        
        if category_id is not None:
            try:
                print("Attempting to fetch category with ID:", category_id)
                category = ArticleCategory.objects.get(id=category_id)
                print("Found category:", category)
                article.category = category
                article.save()
                print("Article updated with category")
            except ArticleCategory.DoesNotExist:
                print("Category not found with ID:", category_id)
                article.category = None
                article.save()
                print("Article category set to None")
                
        return article

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "tags",
            "estimated_reading_time",
            "author_info",
            "views",
            "description",
            "body",
            "banner_image",
            "average_rating",
            "bookmarks_count",
            "bookmarks",
            "claps_count",
            "article_responses",
            "article_responses_count",
            "created_at",
            "updated_at",
            "category",
            "category_id",
            "status",
            "start_date",
            "end_date",
            "is_published",
        ]
        read_only_fields = ["author_info"]


class ClapSerializer(serializers.ModelSerializer):
    article_title = serializers.CharField(source="article.title", read_only=True)
    username = serializers.CharField(source="user.profile.username", read_only=True)

    class Meta:
        model = Clap
        fields = ["id", "username", "article_title"]
