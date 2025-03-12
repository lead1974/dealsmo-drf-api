from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from core_apps.articles.models import Article


@registry.register_document
class ArticleDocument(Document):
    id = fields.KeywordField()
    slug = fields.KeywordField()
    title = fields.TextField(attr="title")
    description = fields.TextField(attr="description")
    body = fields.TextField(attr="body")
    author_username = fields.TextField()
    author_email = fields.TextField()
    tags = fields.KeywordField()

    class Index:
        name = "articles"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

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
