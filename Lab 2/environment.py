import random
class Environment:
    def __init__(self, size=100, bio_hazard_number=5000):
        self.size = size
        self.bio_hazard_number = bio_hazard_number
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.non_accessible_info = {  #(x, y):(h, w)
            (2, 3):(15, 14),
            (30, 70):(7, 7),
            (10, 40):(14, 16),
            (52, 5):(12, 13),
            (80, 3):(10, 12),
            (80, 80):(10, 10),
            (45, 57):(12, 15)
        }
        self.non_accessible = []
        self.bio_hazard = []
        self.generate_non_accessible()
        self.generate_bio_hazard()

    def non_accessible_area(self, h, w, x, y):
        coordinate_list = []
        for i in range(x, w+x+1):
            for j in range(y, h+y+1):
                if i<self.size and j<self.size:
                    coordinate_list.append((i, j))
        return coordinate_list

    def generate_non_accessible(self):
        for (x, y), (h, w) in self.non_accessible_info.items():
            area = self.non_accessible_area(h, w, x, y)
            self.non_accessible.append(area)
            for (i, j) in area:
                self.grid[i][j] = -1

    def generate_bio_hazard(self):
        count = 0
        while count<self.bio_hazard_number:
            x = random.randint(0, self.size-1)
            y = random.randint(0, self.size-1)
            if self.grid[x][y] == 0:
                self.grid[x][y] = 1
                self.bio_hazard.append((x, y))
                count+= 1
#Accessible -> 0 non-Accessible-> -1 bio-hazard -> 1
    def is_accessible(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.grid[x][y] != -1
        return False

    def has_bio_hazard(self, x, y):
        return self.grid[x][y] == 1

    def show_environment(self):
        print("Accessible co-ordinates: ")
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    print(f"({i}, {j})", end=" ")
        print()
        print("Non-accessible co-ordinates: ")
        for j in self.non_accessible:
            for i in j:
                print(f"({i[0]}, {i[1]})", end=" ")
        print()
        print("Co-ordinates of Bio-Hazards:")
        for i in self.bio_hazard:
            print(f"({i[0]}, {i[1]})", end=" ")