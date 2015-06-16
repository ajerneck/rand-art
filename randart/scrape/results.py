from scrape.models import Article
from scrape.models import Result

import collections
import random

def groupArticles(x):
    ## group article keys by label.
    ss = collections.defaultdict(list)
    for i in x:
        ss[i.label].append(i.article_id)

    return ss

def sampleWithin(x, size):
    ## sample article keys within label
    for k in x.keys():
        ## take a sample of size size, or, the whole list if it is smaller.
        ## TODO: size should be proportional to group size.
        l = min([len(x[k]), size])
        x[k] = random.sample(x[k], l)
    return x

## TODO: refactor out the call to results, then limited and stratifiedSample can be the same function.
def limitedStratifiedSample(size, labels):
    x = Result.objects.filter(label__in=labels)

    ss = groupArticles(x)
    ss = sampleWithin(ss, size)

    return ss

def stratifiedSample(size):

    x = Result.objects.all()

    ss = groupArticles(x)
    ss = sampleWithin(ss, size)

    return ss
