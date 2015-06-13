from django.core.management.base import BaseCommand
from scrape.models import Article
import longform

class Command(BaseCommand):
    help = 'populate the article database by scraping'

    def handle(self, *args, **options):
        print('deleting database')
        Article.objects.all().delete()
        print('scraping...')
        arts = longform.scrape()
        for a in arts:
            x = Article(title=a['title'], text=a['text'])
            x.save()
