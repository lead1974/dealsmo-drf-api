from celery import shared_task
from django.utils import timezone
import logging
from .models import Article

logger = logging.getLogger(__name__)

@shared_task
def check_and_update_article_statuses():
    """
    Periodic task to check and update article statuses based on their start_date and end_date.
    - Articles with start_date <= now and status='draft' will be published
    - Articles with end_date <= now and status='published' will be archived
    """
    now = timezone.now()
    logger.info(f"Checking article statuses at {now}")
    
    # Get all articles that should be published (start_date <= now and status is draft)
    articles_to_publish = Article.objects.filter(
        status=Article.Status.DRAFT,
        start_date__lte=now
    )
    
    # Get all articles that should be archived (end_date <= now and status is published)
    articles_to_archive = Article.objects.filter(
        status=Article.Status.PUBLISHED,
        end_date__lte=now
    )
    
    logger.info(f"Found {articles_to_publish.count()} articles to publish")
    logger.info(f"Found {articles_to_archive.count()} articles to archive")
    
    # Publish articles that have reached their start date
    published_count = 0
    for article in articles_to_publish:
        logger.info(f"Publishing article: {article.title}")
        logger.info(f"  - Start date: {article.start_date}")
        logger.info(f"  - Current time: {now}")
        article.status = Article.Status.PUBLISHED
        article.save()
        published_count += 1
    
    # Archive articles that have passed their end date
    archived_count = 0
    for article in articles_to_archive:
        logger.info(f"Archiving article: {article.title}")
        logger.info(f"  - End date: {article.end_date}")
        logger.info(f"  - Current time: {now}")
        article.status = Article.Status.ARCHIVED
        article.save()
        archived_count += 1
    
    logger.info(f"Published {published_count} articles")
    logger.info(f"Archived {archived_count} articles")
    return f"Published {published_count} articles and archived {archived_count} articles" 