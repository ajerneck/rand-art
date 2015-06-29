from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django import forms
from django.shortcuts import render

from scrape.models import Article
from scrape.models import Rating


import collections
import random

import results

def index(request):
    return HttpResponse("""
    <p>
    Welcome to Randart, a site for exploring new and exciting content.
    </p>
    <a href=/rate> Begin by rating some articles </a>
    """)

def inspect(request):
    ss = results.stratifiedSample(10)

    ## create a dict with lists of article objects corresponding to the sample.
    rs = {}
    for label in ss.keys():
        rs[label] = Article.objects.filter(id__in=ss[label])

    ## present sample using a template.
    template = loader.get_template('scrape/inspect.html')
    context = RequestContext(request, {'rs': rs})

    return HttpResponse(template.render(context))

## transform ratings in the form format to a numeric format.
def transform_rating(rating):
    if rating == 'on':
        r = 1
    else:
        r = 0
    return r

def rate(request):
    if request.method == 'POST':
        form = request.POST

        ## get the ratings.
        ## ratings are in the form ('rating_label.id_article.id', 'on'),
        ## for labels with checked checkboxes.
        ## So, split out the article and label id,
        ## so it can be used in creating Ratings below.
        ks = form.items()
        ks = [(k.split('_'),v) for (k,v) in ks if 'rating_' in k]

        ## store ratings in database so they can be used in recommend view.
        rs = [Rating(label=int(k[1]), rating=transform_rating(v)) for (k,v) in ks]
        Rating.objects.all().delete()
        Rating.objects.bulk_create(rs)

        return HttpResponseRedirect('/recommend')

    else:
        ss = results.stratifiedSample(1)
        rs = {}
        for label in ss.keys():
            rs[label] = Article.objects.filter(id__in=ss[label])[0]

    return render(request, 'scrape/rate.html', {'rs': rs})

def recommend(request):
 
    lbls = [i.label for i in Rating.objects.filter(rating=1)]
    ss = results.stratifiedSample(1)

    to_rm = [k for k in ss.keys() if k not in lbls]

    for k in to_rm:
        del(ss[k])

    rs = {}
    for label in ss.keys():
        rs[label] = Article.objects.filter(id__in=ss[label])

    template = loader.get_template('scrape/inspect.html')
    context = RequestContext(request, {'rs': rs})

#    return HttpResponse(str(to_rm))
    return HttpResponse(template.render(context))
