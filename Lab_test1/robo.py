class robo:
    def __init__(self):
        self.right = 0
        self.left = 0
        self.up = 0
        self.down = 0
        self.objet_colleted = 0
        self.movement_track = []
    def move_right(self, x):
        if x==99:
            return x
        elif self.right == 1:
            return x
        else:
            x+=1
            self.right = 1
            self.left = 0
            self.up = 0
            self.down = 0
            self.movement_track.append('right')
            return x
    def move_left(self, x):
        if x==0 :
            return x
        elif self.left == 1:
            return x
        else:
            x-=1
            self.right = 0
            self.left = 1
            self.up = 0
            self.down = 0
            self.movement_track.append('left')
            return x
    def move_up(self, y):
        if y==99:
            return y
        elif self.up == 1:
            return y
        else:
            y+=1
            self.right = 0
            self.left = 0
            self.up = 1
            self.down = 0
            self.movement_track.append('up')
            return y
    def move_down(self, y):
        if y==0:
            return y
        elif self.down == 1:
            return y
        else:
            y-=1
            self.right = 0
            self.left = 0
            self.up = 0
            self.down = 1
            self.movement_track.append('down')
            return y
    def collect_objects(self):
        self.objet_colleted += 1


