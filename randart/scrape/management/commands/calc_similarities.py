from django.core.management.base import BaseCommand

from scrape.models import Article
from scrape.models import Result

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans


def calc():
    print('Querying...')
    a = Article.objects.raw('SELECT * FROM scrape_article WHERE LENGTH(text) > 1000 limit 4000')
    ts =  [x.text for x in a]

    print('Extracting features...')
    count_vect = CountVectorizer(stop_words='english', min_df=2)
    word_counts = count_vect.fit_transform(ts)

    tf_transformer = TfidfTransformer()
    tfidf = tf_transformer.fit_transform(word_counts)
    print('Matrix shape: '+  str(tfidf.shape))

    ## make a list of models here, with:
    ## different similarity measures, different methods.
    ## should be a grid, then, save all the results, then, evaluate all the results:
    ## ie, look at at sample of articles, see how they fare in the different modelss.
    ## also build a tool to list a sample from each cluster, with url, title, and first couple of paragraphs.

    print('Running Truncated SVD (LSA) to reduce dimensionality')
    svd = TruncatedSVD(n_components = 200)
    x = svd.fit_transform(tfidf)

    print('Fitting model...')
    model = KMeans(20, init='k-means++', max_iter=100, n_init=1,)
    model.fit(x)

    print('Saving results...')
    Result.objects.all().delete()
    xs = zip(a, model.labels_)
    rs = [Result(article=x, label=i, learner="kmeans, clusters=10, x=tfidf") for (x, i) in xs ]
    Result.objects.bulk_create(rs)

class Command(BaseCommand):
    help = 'calculate similarities between documents'

    def handle(self, *args, **options):
        calc()
