import matplotlib.pyplot as plt
import time
from config import *
from Application import database, rating, elommr as mmr
from Utilities import practiscore as ps

division = 'Carry Optics'
match_num = 205465
file = root + '/Data/jsonFiles/' + str(match_num) + '.json'

# M = 0
# scores = rating.match_update(file, division)
#
# for score in scores:
#     print(score.first, score.last, 'Performance:', score.performance, 'New Rating:', score.rating)


path = root + '/Data/jsonFiles/'
dir_list = os.listdir(path)
t = time.time()

for file in dir_list:
    t2 = time.time()
    print('Match:', file)
    file = path + file
    rating.match_update(file, division)
    print('Elapsed Time (s): %s' % (np.round(time.time() - t, 3)))
    print('Elapsed Time (s) for match: %s' % (np.round(time.time() - t2, 3)))


## Ranked list
shooters = database.get_unique_competitors(division)
competitors = list()
for shooter in shooters:
    try:
        competitors.append(database.get_competitor_current(shooter[0], division)[0])
    except:
        pass

competitors.sort(key=lambda x: x[2], reverse=True)
for competitor in competitors:
    print(competitor)

## Skill tracking plot
shooters = ['L5336', 'A117077', 'TY99488', 'A128439', 'A142166', 'A104773']
history = list()
for shooter in shooters:
    history.append(database.get_competitor_history(shooter, division))

fig, ax = plt.subplots()
for shooter in history:
    t = list()
    skill, performance, uncertainty = list(), list(), list()
    shooter.sort(key=lambda x: x[5], reverse=True)

    for event in shooter:
        t.append(datetime.datetime.fromtimestamp(event[5]))
        skill.append(event[2])
        uncertainty.append(event[3])
        performance.append(event[4])
    ax.plot(t, skill, label=shooter[0][0] + ' ' + shooter[0][1])
fig.autofmt_xdate()
plt.legend()
plt.show()

# skillA = 1580
# skillB = 1500
# uncertainty = 350
# diff = 10
#
# t = time.time()
# x = np.linspace(rating_min, rating_max, rating_max - rating_min + 1)
# loss = mmr.loss_distribution(x, skillA, uncertainty)
# win = mmr.win_distribution(x, skillB, uncertainty)
#
#
# diff_win = mmr.logistic(diff)
# win_draw = diff_win * win + (1 - diff_win) * loss
#
# print('Elapsed Time (s): %s' % (np.round(time.time() - t, 3)))
# print('Win/Draw Ratio @', str(diff) + '%:', diff_win)
# print('Performance:', x[np.argmin(np.abs(win_draw))])
#
# N = int(np.round((rating_max - rating_min + 1) / 25, 0))
# x2 = np.linspace(rating_min, rating_max, N)
# y = np.zeros(N)
# for i in range(N):
#     print(np.round(i / N * 100, 2), '%')
#     loss = mmr.loss_distribution(x, x2[i], uncertainty)
#     win = mmr.win_distribution(x, skillB, uncertainty)
#     win_draw = diff_win * win + (1 - diff_win) * loss
#     y[i] = x[np.argmin(np.abs(win_draw))] - x2[i]
#
# print('Break even:', x2[np.argmin(np.abs(y))])
# plt.plot(x, loss, label='draw')
# plt.plot(x, win, label='win')
# plt.plot(x, win_draw, label='Combo')
# plt.plot(x, cdf, label='cdf')
# # plt.plot(x2, y)
# x = np.linspace(1, 300, 1000)
#
#
# def ratio(val, k):
#     return (mmr.logistic(val - 1, scale=k) - 0.5) * 3 + 0.1
#
#
# def numbers(val, slope, ymin, ymax):
#     y = val * slope + ymin
#     if y > ymax:
#         return ymax
#     else:
#         return y
#
#
# y = ratio(x, competitor_count_factor)
# plt.plot(x, y)
# plt.legend()
# plt.show()

print('')
print('Target Destroyed')
