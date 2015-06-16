from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django import forms
from django.shortcuts import render
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

# class RateForm(forms.Form):
  
#     a = forms.CharField(label = 'testing')

def rate(request):
    if request.method == 'POST':
        form = request.POST
        return HttpResponseRedirect('/recommend')

    else:
        ss = results.stratifiedSample(1)
        rs = {}
        for label in ss.keys()[0:2]:
            rs[label] = Article.objects.filter(id__in=ss[label])[0]

    return render(request, 'scrape/rate.html', {'rs': rs})
 
def recommend(request):
    return HttpResponse('recommendations')


# def rate2(request):
#     ss = results.stratifiedSample(1)
#     rs = Article.objects.filter(id__in=ss.values())
#     template = loader.get_template('scrape/rate.html')

#     # I AM HERE: implement a form that allows the user to rate each article.
#     # very similar to index.html, but, just with a radio button for each of yes, no.

#     # then, based on the results, select more articles from those clusters, or, articles that are similar to those.
