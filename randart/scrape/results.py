from scrape.models import Article
from scrape.models import Result

import collections
import random

def stratifiedSample(size):

    x = Result.objects.all()

    ## group article keys by label.
    ss = collections.defaultdict(list)
    for i in x:
        ss[i.label].append(i.article_id)

    ## sample article keys within label
    for k in ss.keys():
        ## take a sample of size size, or, the whole list if it is smaller.
        ## TODO: size should be proportional to group size.
        l = min([len(ss[k]), size])
        ss[k] = random.sample(ss[k], l)

    return ss
