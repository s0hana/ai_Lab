import random
import cv2
import numpy as np
def non_accessible_area(h, w, x, y):
    co_ordinate_list = []
    for i in range(x, w+x+1):
        for j in range(y, h+y+1):
            if i < 100 and j<100:
                co_ordinate_list.append((i, j))
    return co_ordinate_list
environment = [[0 for _ in range(100)] for _ in range(100)]
#print(environment)
non_accessible_info = {        #(x, y):(h, w)
    (2, 3):(15, 14),
    (30, 70):(7, 7),
    (10, 40):(14, 16),
    (52, 5): (12, 13),
    (80, 3): (10, 12),
    (80, 80): (10, 10), 
    (45, 57):(12, 15)
}
non_accessible = []
for (x, y), (h, w) in non_accessible_info.items():
    non_accessible.append(non_accessible_area(h, w, x, y))
#print(non_accessible)
for i in non_accessible:
    for j in i:
        s, t = j
        environment[s][t] = -1
bio_hazard_number = 150
bio_hazard = []
count_hazard = 0
while True:
    _x = random.randint(0, 99)
    _y = random.randint(0, 99)
    if environment[_x][_y] == 0:
        environment[_x][_y] = 1
        bio_hazard.append((_x, _y))
        count_hazard+=1
        if count_hazard==bio_hazard_number:
            break
print(environment)
print("Co-ordinates of bio-hazard materials: ")
for i in bio_hazard:
    print(i, end=" ")
print("Co-ordinates of non-accessible points: ")
for k in non_accessible:
    for j in k:
        print(j, end=" ")
print("Co-ordinates of accessible points: ")
for x in range(100):
    for y in range(100):
        if environment[x][y]!=-1:
            print(f"({x}, {y})", end=" ")
img = np.zeros((100, 100, 3), dtype=np.uint8)
for i in range(100):
    for j in range(100):
        if environment[i][j] == -1:
            img[i][j] = (0, 0, 0)
        elif environment[i][j] == 1:
            img[i][j] = (0, 0, 255)
        else:
            img[i][j] = (255, 255, 255)
img = cv2.resize(img, (600, 600), interpolation=cv2.INTER_NEAREST)
cv2.imshow("Environment Grid", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("environment.png", img)