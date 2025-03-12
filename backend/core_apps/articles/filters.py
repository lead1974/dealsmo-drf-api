import django_filters as filters
from django.utils import timezone
from core_apps.articles.models import Article


class ArticleFilter(filters.FilterSet):
    author = filters.CharFilter(
        field_name="author__first_name", lookup_expr="icontains"
    )
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    tags = filters.CharFilter(field_name="tags__name", lookup_expr="iexact")
    created_at = filters.DateFromToRangeFilter(field_name="created_at")
    updated_at = filters.DateFromToRangeFilter(field_name="updated_at")
    status = filters.ChoiceFilter(choices=Article.Status.choices)
    start_date = filters.DateFromToRangeFilter(field_name="start_date")
    end_date = filters.DateFromToRangeFilter(field_name="end_date")
    is_active = filters.BooleanFilter(method='filter_is_active')
    category_id = filters.UUIDFilter(field_name="category__id")
    category_slug = filters.CharFilter(field_name="category__slug")

    def filter_is_active(self, queryset, name, value):
        now = timezone.now()
        if value:
            return queryset.filter(
                status=Article.Status.PUBLISHED,
                start_date__lte=now,
                end_date__gt=now
            )
        return queryset

    class Meta:
        model = Article
        fields = [
            "author", 
            "title", 
            "tags", 
            "created_at", 
            "updated_at",
            "status",
            "start_date",
            "end_date",
            "is_active",
            "category_id",
            "category_slug",
        ]
