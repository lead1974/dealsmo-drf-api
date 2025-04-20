from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from core_apps.articles.models import Article


@registry.register_document
class ArticleDocument(Document):
    id = fields.KeywordField()
    slug = fields.KeywordField()
    title = fields.TextField(
        attr="title",
        analyzer='standard',
        fields={
            'raw': fields.KeywordField(),
            'ngram': fields.TextField(analyzer='ngram_analyzer')
        }
    )
    description = fields.TextField(
        attr="description",
        analyzer='standard',
        fields={
            'raw': fields.KeywordField(),
            'ngram': fields.TextField(analyzer='ngram_analyzer')
        }
    )
    body = fields.TextField(
        attr="body",
        analyzer='standard',
        fields={
            'raw': fields.KeywordField(),
            'ngram': fields.TextField(analyzer='ngram_analyzer')
        }
    )
    author_username = fields.TextField(
        analyzer='standard',
        fields={'raw': fields.KeywordField()}
    )
    author_email = fields.TextField(
        analyzer='standard',
        fields={'raw': fields.KeywordField()}
    )
    tags = fields.KeywordField()

    class Index:
        name = "articles"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "analyzer": {
                    "standard": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "asciifolding", "word_delimiter", "trim", "snowball"]
                    },
                    "ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "asciifolding", "ngram_filter"]
                    }
                },
                "filter": {
                    "ngram_filter": {
                        "type": "ngram",
                        "min_gram": 3,
                        "max_gram": 4
                    }
                }
            }
        }

    class Django:
        model = Article
        fields = ["created_at"]

    def prepare_author_username(self, instance):
        return instance.author.profile.username

    def prepare_author_email(self, instance):
        return instance.author.email

    def prepare_tags(self, instance):
        if isinstance(instance.tags, list):
            return instance.tags
        return [tag.name for tag in instance.tags.all()]

    def prepare_id(self, instance):
        return str(instance.id)

    def prepare_slug(self, instance):
        return instance.slug
