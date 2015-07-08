"""
Clustering books using networks of co-ratership.

This module creates a one-mode network of books by collapsing the two-mode
network of books and users, tied to gether by their ratings.
Books that have at least one user rating both in common are tied together.

The main problem is that many path-finding algorithms (which would otherwise be
used to create a distance matrix for clustering) do not scale well.

So, the one-mode adjancency sparse matrix between books is converted to an
edgelist, then to an igraph network object.

Efficient community-detection algorithms, such as fast_greedy are used.

The dataset used, the Book-Crossing Dataset, is available here:
http://www2.informatik.uni-freiburg.de/~cziegler/BX/

"""

import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
import random
import igraph

## toy dataset.
import toy

ratings = toy.ratings

ratings = pd.read_csv('/home/alexander/data/data-science/book-crossing/BX-Book-Ratings.csv', sep=';')

## TODO: delete books with only n raters? NO: delete books that are isolates in the book_mode graph.

ratings = ratings[ratings['Book-Rating'] != 0]

## remove users who have only rated one book.
br = ratings.groupby('User-ID').count()['ISBN']
br = br[br != 1]
ratings = ratings[ratings['User-ID'].isin(br.index)]

## downsample.
books = ratings['ISBN'].unique()
rows = random.sample(books, int(len(books)*.20 ))
ratings = ratings[ratings['ISBN'].isin(rows)]

ids_books= dict([(ix,isbn) for ix, isbn in enumerate(ratings['ISBN'].unique())])
books_ids = dict((v,k) for k,v in ids_books.iteritems())

ids = [books_ids[i] for i in ratings['ISBN']]

# 'invert' the rating, so that high ratings become low edge weights.
ratings['rating'] = 10 -ratings['Book-Rating']

## create sparse, two-mode incidence matrix of ratings between users and books.
two_mode = coo_matrix((ratings['rating'], (ids, ratings['User-ID'])))
two_mode = two_mode.tocsr()
## rows are books, columns are users.

## multiply the two-mode matrix by its transpose to get a one-mode matrix of ratings between books.
book_mode = two_mode.dot(np.transpose(two_mode))
# users = np.transpose(a).dot(a)

## use the indices of the nonzero values to convert sparse matrix to sparse edgelist.
nz = book_mode.nonzero()

## generate edgelist without duplicate and self-edges.
## duplicates come from that the adjancency matrix has both i,j and j,i entries,
##        and that they are the same, because the graph is undirected.
el = {}
for i, j, v in zip(nz[0], nz[1], book_mode.toarray()[nz]):
    if j != i and (j, i) not in el:
        el[(i,j)] = v

## convert to edgelist format suitable for igraph by unpacking the first tuple.
ell = [(k[0],k[1],v) for k,v in el.iteritems()]

g = igraph.Graph.TupleList(ell, directed=False, weights=True)


## use the fast_greedy algorithm, because it is supposed to have almost linear complexity.
com_fast_greedy = g.community_fastgreedy(weights='weight')

## TODO: use community_multilevel too, see how it compares.


## extract clusters as the vertice memberships at the maximal modularity level.
results = pd.DataFrame(zip(g.vs.indices, com_fast_greedy.as_clustering(n=100).membership), columns=['id', 'cluster'])
results['algorithm'] = 'fast_greedy'

## merge in isbns
results['ISBN'] = pd.Series(ids_books[i] for i in results['id'])


# evaluate clustering by examining book title and authors
book_data = pd.read_csv('/home/alexander/data/data-science/book-crossing/BX-Books-utf8.csv', sep=';')
book_data['author'] = book_data['Book-Author'].str.lower()
book_data['title'] = book_data['Book-Title'].str.lower()

## merging in book data.
results = results.merge(book_data, on='ISBN')

## evaluate clusters
for n, g in results.groupby(['cluster']):
    print '----------------'
    print 'cluster %s' % n
    print g.count()['title']

## most popular authors by cluster.
## authors should be normalized by their total numbers.
for n, g in results[results['cluster'] > 1000 ].groupby('cluster'):
    print '----------------'
    print g.groupby('cluster').count()['title']
    print pd.Series(g.groupby('author').count()['title']).order(ascending=False).head(10)


## actual title and author of books in some clusters.
pd.set_option('display.max_colwidth', 1000)
for n, g in results[results['cluster'] < 25].groupby('cluster'):
    print '-----------------'
    print 'cluster: %s ' % n
    print g.groupby('cluster').count()['title']
    print '\t', book_data[book_data['ISBN'].isin(g['ISBN'][0:100])][['Book-Title','Book-Author']].to_string()
