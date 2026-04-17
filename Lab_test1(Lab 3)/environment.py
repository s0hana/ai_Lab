import numpy as np
import random
def make_building(x, y, h, w):
    obs = []
    for i in range(x, w+1):
        for j in range(y, h+1):
            obs.append((i, j))
    return obs
grid = np.zeros((100, 100), dtype=int)
#print(grid)
obs_dict = {                #x, y, h, w
    (2, 3): (12, 15),
    (30, 33):(13, 13),
    (67, 88): (10, 15),
}
restricted_area = []
for c, v in obs_dict.items():
    x1, y1 = v
    h1, w1 = c
    restricted_area.append(make_building(x1, y1, h1, w1))
#print(restricted_area)
for _p in restricted_area:
    for _i in _p:
        n, m = _i
        grid[n][m] = 1
#print(grid.ndim)
object_number = 150
_object_number = 0
while True:
    _x = random.randint(0, 99)
    _y = random.randint(0, 99)
    if grid[_x][_y] == 0:
        _object_number += 1
        grid[_x][_y] = -1
    if _object_number == object_number:
        break
print("Object Co-ordinates:")
for i in range(100):
    for j in range(100):
        if grid[i][j] == -1:
            print(f"({i}, {j})", end=" ")
print()
print("Obstacles Co-ordinates:")
for i in range(100):
    for j in range(100):
        if grid[i][j] == 1:
            print(f"({i}, {j})", end=" ")
#print(grid)