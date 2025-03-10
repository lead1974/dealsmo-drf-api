from django.core.management.base import BaseCommand
from django_elasticsearch_dsl.registries import registry

from core_apps.articles.models import Article


class Command(BaseCommand):
    help = "Create and populate Elasticsearch indices"

    def handle(self, *args, **options):
        for doc in registry.get_documents():
            self.stdout.write(f"Creating index for {doc._doc_type.model.__name__}")
            doc().update()
            self.stdout.write(self.style.SUCCESS(f"Index created for {doc._doc_type.model.__name__}")) 