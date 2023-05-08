from Application import elo
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


match = {'name': ['Riley', 'Dyami', 'Kirt', 'Sean', 'Dana'], 'score': [100., 93.19, 86.59, 79.37, 50.48], 'rating': [1000, 1000, 1000, 1000, 500]}
df = pd.DataFrame(data=match)

scores = df.score
ratings = df.rating

N_matches = 100
x = np.linspace(0, N_matches, N_matches + 1)

print('initial expected:', elo.expected_scores(ratings))
print('initial expected new:', elo.expected2(ratings, scale=1000))
print('initial scores:', elo.scores_normalized(scores, method='percent'))

riley = [ratings[0]]
dyami = [ratings[1]]
kirt = [ratings[2]]
sean = [ratings[3]]
dana = [ratings[4]]


def kfactor(number, maxval=500):
    if number > 10:
        return 10
    return maxval / (number + 1)


new_ratings = ratings
for i in range(N_matches):
    k = kfactor(i, 300)
    # if i > 2:
    #     scores = scores / 2
    #     scores[0] = 100
    new_ratings = elo.rating_adjustment(new_ratings, scores, k=k, scale=1000)
    riley.append(new_ratings[0])
    dyami.append(new_ratings[1])
    kirt.append(new_ratings[2])
    sean.append(new_ratings[3])
    dana.append(new_ratings[4])

print(new_ratings)
print('expected', elo.expected_scores(new_ratings))
print('actual', elo.scores_normalized(scores))

plt.plot(x, riley, label='Riley')
plt.plot(x, dyami, label='Dyami')
plt.plot(x, kirt, label='Kirt')
plt.plot(x, sean, label='Sean')
plt.plot(x, dana, label='Dana')


def expected(Ra, Rb, D=400):
    return 1 / (1 + 10 ** ((Rb - Ra) / D))

Rb = 1000
x = np.linspace(100, 2000, 10000)
y = expected(x, Rb, 400)

# plt.plot(x, y)

plt.legend()
plt.show()

