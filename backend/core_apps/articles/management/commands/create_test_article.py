from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from core_apps.articles.models import Article

class Command(BaseCommand):
    help = 'Creates a test published article'

    def handle(self, *args, **options):
        User = get_user_model()
        author = User.objects.first()
        
        if not author:
            self.stdout.write(self.style.ERROR('No users found in the database'))
            return
            
        article = Article.objects.create(
            author=author,
            title='Test Published Article',
            description='Test Description',
            body='Test Body',
            status='published',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30)
        )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created test article: {article.title}')) 