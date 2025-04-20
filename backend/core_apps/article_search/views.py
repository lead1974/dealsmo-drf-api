from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import permissions
from elasticsearch_dsl import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from elasticsearch import Elasticsearch
from django.conf import settings

from .documents import ArticleDocument
from .serializers import ArticleElasticSearchSerializer


@extend_schema(
    tags=['search'],
    parameters=[
        OpenApiParameter(
            name='search',
            description='Search query string to search in title, description, body, author info, and tags',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='tags',
            description='Filter by tags (comma-separated)',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='ordering',
            description='Sort by field (e.g. created_at or -created_at for descending)',
            required=False,
            type=str
        )
    ]
)
class ArticleElasticSearchView(DocumentViewSet):
    document = ArticleDocument
    serializer_class = ArticleElasticSearchSerializer
    lookup_field = "id"
    permission_classes = [permissions.AllowAny]

    filter_backends = [
        # FilteringFilterBackend,
        # IdsFilterBackend,
        # OrderingFilterBackend,
        # DefaultOrderingFilterBackend,
        # SearchFilterBackend,
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
            # Create a multi_match query for all search fields with fuzzy matching
            query = Q(
                'multi_match',
                query=search,
                fields=[
                    'title^3',
                    'title.ngram^2',
                    'description^2',
                    'description.ngram',
                    'body',
                    'body.ngram',
                    'author_username',
                    'author_email',
                    'tags'
                ],
                type='most_fields',
                fuzziness='AUTO:4,6',
                minimum_should_match='30%',
                operator='or',
                tie_breaker=0.3
            )
            queryset = queryset.query(query)
            
            # Add debug logging
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Search query: {search}")
            logger.info(f"Elasticsearch query: {query.to_dict()}")
            
            # Log the raw response for debugging
            raw_response = queryset.execute()
            logger.info(f"Raw response: {raw_response.to_dict()}")
            logger.info(f"Total results before collapse: {raw_response.hits.total.value}")
            
            # Log each hit for debugging
            for hit in raw_response.hits:
                logger.info(f"Hit score: {hit.meta.score}")
                logger.info(f"Hit title: {hit.title}")
                logger.info(f"Hit body excerpt: {hit.body[:200] if hit.body else 'No body'}")
        
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            queryset = queryset.query('terms', tags=tag_list)
        
        # Log the final queryset
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Final queryset: {queryset.to_dict()}")
        logger.info(f"Final queryset count: {queryset.count()}")
            
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search = request.query_params.get('search', None)
        
        if search:
            # Execute the search and get raw results
            response = queryset.execute()
            
            # Log the raw response for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Raw response: {response.to_dict()}")
            logger.info(f"Total results: {response.hits.total.value}")
            
            # Process the results
            results = []
            for hit in response.hits:
                results.append({
                    'id': hit.id,
                    'title': hit.title,
                    'body': hit.body[:200] if hit.body else '',
                    'score': hit.meta.score,
                    'tags': hit.tags if hasattr(hit, 'tags') else []
                })
            
            return Response({
                'count': response.hits.total.value,
                'results': results
            })
        
        # If no search term, use the normal serializer
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class DirectArticleSearchView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        search = request.query_params.get('search', None)
        
        if not search:
            return Response({"count": 0, "results": []})
        
        # Connect to Elasticsearch using the correct setting
        es = Elasticsearch([settings.ELASTICSEARCH_DSL['default']['hosts']])
        
        # Create the search query
        query = {
            "query": {
                "multi_match": {
                    "query": search,
                    "fields": [
                        "title^3",
                        "title.ngram^2",
                        "description^2",
                        "description.ngram",
                        "body",
                        "body.ngram",
                        "author_username",
                        "author_email",
                        "tags"
                    ],
                    "type": "most_fields",
                    "fuzziness": "AUTO:4,6",
                    "minimum_should_match": "30%",
                    "operator": "or",
                    "tie_breaker": 0.3
                }
            }
        }
        
        # Execute the search
        response = es.search(index="articles", body=query)
        
        # Log the response for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Direct Elasticsearch response: {response}")
        
        # Process the results
        results = []
        for hit in response['hits']['hits']:
            results.append({
                'id': hit['_id'],
                'title': hit['_source'].get('title', ''),
                'body': hit['_source'].get('body', '')[:200] if hit['_source'].get('body') else '',
                'score': hit['_score'],
                'tags': hit['_source'].get('tags', [])
            })
        
        return Response({
            'count': response['hits']['total']['value'],
            'results': results
        })
