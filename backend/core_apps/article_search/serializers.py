from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .documents import ArticleDocument


class ArticleElasticSearchSerializer(DocumentSerializer):
    class Meta:
        document = ArticleDocument
        fields = ["id", "slug", "title", "description", "body", "author_username", "author_email", "created_at", "tags"]
