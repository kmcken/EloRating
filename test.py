from Application import elo
import pandas as pd
import numpy as np


scores = {'name': ['Riley', 'Dyami', 'Kirt', 'Sean', 'Dana'], 'score': [100., 93.19, 86.59, 79.37, 50.48], 'rating': [1500, 1400, 1100, 1000, 600]}
df = pd.DataFrame(data=scores)

K = 0
k = elo.k_factor(K)

Ra = 1500
Rb = 1400

print(elo.expected_score(Ra, Rb))
print(elo.logistic_score(7, 10))
print(k)

scores = np.array([100., 93.19, 86.59, 79.37, 50.48])
ratings = np.array([1300, 1200, 1100,  950, 500])
ks = np.array([elo.k_factor(K), elo.k_factor(K), elo.k_factor(K), elo.k_factor(K), elo.k_factor(K)])
print('Performance Rating')
print((elo.performance_rating(ratings, scores)))

print('New Rating')
for i in range(0, 15):
    ratings = ratings + elo.rating_adjustment(ratings, scores, ks)
    print(ratings)

