from django.http import HttpResponse
from scrape.models import Article


def index(request):
    n = len(Article.objects.all())
    return HttpResponse('There are ' + str(n) + ' articles scraped')
