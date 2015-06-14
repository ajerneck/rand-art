from django.core.management.base import BaseCommand

from scrape.models import Article
from scrape.models import Result

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans


def calc():
    a = Article.objects.all()[1:100]
    ts =  [x.text for x in a]

    count_vect = CountVectorizer(stop_words='english')
    word_counts = count_vect.fit_transform(ts)

    tf_transformer = TfidfTransformer()
    tfidf = tf_transformer.fit_transform(word_counts)

    ## make a list of models here, with:
    ## different similarity measures, different methods.
    ## should be a grid, then, save all the results, then, evaluate all the results:
    ## ie, look at at sample of articles, see how they fare in the different modelss.
    ## also build a tool to list a sample from each cluster, with url, title, and first couple of paragraphs.

 
    model = KMeans(5, init='k-means++', max_iter=100, n_init=1)
    model.fit(tfidf)

    ## associated each article with a label, create result rows, and bulk save.
    ## delete all, but, this should really be more refined: delete where the model is the same as the model now being run.
    Result.objects.all().delete()
    xs = zip(a, model.labels_)
    rs = [Result(article=x, label=i, learner="kmeans, clusters=5, x=tfidf") for (x, i) in xs ]
    Result.objects.bulk_create(rs)


class Command(BaseCommand):
    help = 'calculate similarities between documents'

    def handle(self, *args, **options):
        calc()
