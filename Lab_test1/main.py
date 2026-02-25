import environment
import robo
import random
r = robo.robo()
#position_robo = [0, 0]
dirt_grid = environment.grid
#print(dirt_grid)
x = 0
y = 67
for i in range(100):
    for j in range(100):
        if dirt_grid[i][j] == -1:
            x = i
            y = j
            break
count = 0
while True:
    random_number = random.randint(0,3) #0->left, 1-> right, 2->up, 3->down
    #print(random_number)
    if random_number == 0:
        if dirt_grid[x][y] == -1:
            dirt_grid[x][y] = 0
            r.collect_objects()
        x = r.move_left(x)
    elif random_number == 1:
        if dirt_grid[x][y] == -1:
            dirt_grid[x][y] = 0
            r.collect_objects()
        x = r.move_right(x)
    elif random_number == 2:
        if dirt_grid[x][y] == -1:
            dirt_grid[x][y] = 0
            r.collect_objects()
        y = r.move_up(y)
    else:
        if dirt_grid[x][y] == -1:
            r.collect_objects()
            dirt_grid[x][y] = 0
        y = r.move_down(y)
    count+=1
    if count == 500:
        break
print("Object Collected: ")
print(r.objet_colleted)
print("Movements: ")
print(r.movement_track)
