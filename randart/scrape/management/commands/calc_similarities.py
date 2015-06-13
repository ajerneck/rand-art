from django.core.management.base import BaseCommand

from scrape.models import Article

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans


def calc(clusters):
    a = Article.objects.all()
    ts =  [x.text for x in a]

    count_vect = CountVectorizer(stop_words='english')
    word_counts = count_vect.fit_transform(ts)

    tf_transformer = TfidfTransformer()
    tfidf = tf_transformer.fit_transform(word_counts)

    model = KMeans(clusters, init='k-means++', max_iter=100, n_init=1)
    model.fit(tfidf)

    for i, x in enumerate(a):
        x.label = model.labels_[i]
        x.save()

    #return {'db': a, 'tfidy': tfidf, 'model':model}



class Command(BaseCommand):
    help = 'calculate similarities between documents'

    def handle(self, clusters, *args, **options):
        calc(int(clusters))
