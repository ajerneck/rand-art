from scrape.models import Article
from scrape.models import Result

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

from sklearn.decomposition import TruncatedSVD

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

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
model = KMeans(20, init='k-means++', max_iter=100, n_init=1)
model.fit(x)

## associated each article with a label, create result rows, and bulk save.
## delete all, but, this should really be more refined: delete where the model is the same as the model now being run.

# print('Running SVD to plot...')
# svd = TruncatedSVD(n_components=2)
# rd = svd.fit(x).fit_transform(x)

# ## make dataframe with docs and clusters
# df = pd.DataFrame()
# df['x'] = rd[0:,0]
# df['y'] = rd[0:,1]
# df['label'] = model.labels_

## plot
# groups = df.groupby('label')
# cols = sns.cubehelix_palette(len(groups))
# g = sns.FacetGrid(df, hue='label', palette=cols)
# g.map(plt.scatter, 'x', 'y')

## most common words per label.


# I AM HERE: use seaborn to make nice plots to visualize the clusters.
# also: calculate most common words per cluster, to understand what each one is about.
# also: use multiple models to compare, eg, cosine vs eacludian distance.




print('Saving results...')
Result.objects.all().delete()
xs = zip(a, model.labels_)
rs = [Result(article=x, label=i, learner="kmeans, clusters=10, x=tfidf") for (x, i) in xs ]
Result.objects.bulk_create(rs)

