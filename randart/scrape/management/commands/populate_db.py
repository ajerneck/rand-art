from django.core.management.base import BaseCommand
from scrape.models import Article
import longform

class Command(BaseCommand):
    help = 'populate the article database by scraping'

    def handle(self, *args, **options):
        print('Deleting database')
        Article.objects.all().delete()
        print('Scraping...')
        arts = longform.scrape()
        ## TODO: can this be made faster? -- yes, use bulk_create.
        print('Saving results...')
        rows = [Article(title=i['title'], url=i['url'], text=i['text']) for i in arts]
        Article.objects.bulk_create(rows)

        # for a in arts:
        #     x = Article(title=a['title'], text=a['text'])
        #     x.save()
