from django.http import HttpResponse
from django.template import RequestContext, loader
from scrape.models import Article

import collections

import results

def index(request):
    ss = results.stratifiedSample(10)

    ## create a dict with lists of article objects corresponding to the sample.
    rs = {}
    for label in ss.keys():
        rs[label] = Article.objects.filter(id__in=ss[label])

    ## present sample using a template.
    template = loader.get_template('scrape/index.html')
    context = RequestContext(request, {'rs': rs})

    return HttpResponse(template.render(context))
