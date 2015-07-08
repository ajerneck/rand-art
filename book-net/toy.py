"""
Toy dataset for developing, testing, and exploring.
"""
import pandas as pd

ratings = pd.DataFrame({'User-ID': [1, 1, 2, 3, 4, 1, 1, 2, 3, 4],
                        'ISBN': ['alpha', 'beta', 'xena', 'xena', 'delta', 'xena', 'delta', 'fox', 'fox', 'epsilon'],
                        'Book-Rating': [1, 2, 2, 3, 4, 1, 3, 3, 8, 8]
})

