from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from rest_framework import permissions
from elasticsearch_dsl import Q

from .documents import ArticleDocument
from .serializers import ArticleElasticSearchSerializer


class ArticleElasticSearchView(DocumentViewSet):
    document = ArticleDocument
    serializer_class = ArticleElasticSearchSerializer
    lookup_field = "id"
    permission_classes = [permissions.AllowAny]

    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    search_fields = (
        "title",
        "description",
        "body",
        "author_username",
        "author_email",
        "tags",
    )
    filter_fields = {
        "slug": "slug",
        "created_at": "created_at",
        "id": "id",
        "author_email": "author_email",
    }

    ordering_fields = {"created_at": "created_at"}
    ordering = ("-created_at",)

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        tags = self.request.query_params.get('tags', None)
        
        if search:
            # Create a multi_match query for all search fields
            query = Q(
                'multi_match',
                query=search,
                fields=self.search_fields,
                type='best_fields'
            )
            queryset = queryset.query(query)
        
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            queryset = queryset.query('terms', tags=tag_list)
        
        # Add collapse to ensure unique results and include top hits
        queryset = queryset.extra(
            collapse={
                'field': 'id',
                'inner_hits': {
                    'name': 'most_recent',
                    'size': 1,
                    'sort': [{'created_at': 'desc'}]
                }
            }
        )
            
        return queryset
