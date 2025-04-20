from django.core.management.base import BaseCommand
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import Q
from core_apps.articles.models import Article
from core_apps.article_search.documents import ArticleDocument

class Command(BaseCommand):
    help = "Verify Elasticsearch search functionality"

    def add_arguments(self, parser):
        parser.add_argument('search_term', type=str, help='Search term to test')

    def handle(self, *args, **options):
        search_term = options['search_term']
        
        # Check database
        self.stdout.write("Checking database...")
        db_count = Article.objects.filter(body__icontains=search_term).count()
        self.stdout.write(f"Found {db_count} articles in database containing '{search_term}'")
        
        if db_count > 0:
            article = Article.objects.filter(body__icontains=search_term).first()
            self.stdout.write(f"Sample article title: {article.title}")
            self.stdout.write(f"Sample article body excerpt: {article.body[:200]}")
        
        # Check Elasticsearch
        self.stdout.write("\nChecking Elasticsearch...")
        doc = ArticleDocument()
        query = Q(
            'multi_match',
            query=search_term,
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
        
        search = doc.search().query(query)
        response = search.execute()
        
        self.stdout.write(f"Found {response.hits.total.value} articles in Elasticsearch")
        
        if response.hits.total.value > 0:
            for hit in response.hits:
                self.stdout.write(f"\nHit score: {hit.meta.score}")
                self.stdout.write(f"Hit title: {hit.title}")
                self.stdout.write(f"Hit body excerpt: {hit.body[:200] if hit.body else 'No body'}")
        
        # Check index settings
        self.stdout.write("\nChecking index settings...")
        es = doc._get_connection()
        index_settings = es.indices.get_settings(index=doc._doc_type.index)
        self.stdout.write("Index settings:")
        self.stdout.write(str(index_settings)) 