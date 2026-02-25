import random
class Robot:
    def __init__(self, environment):
        self.env = environment
        self.size = environment.size
        while True:     #a random accessible position
            self.x = random.randint(0, self.size-1)
            self.y = random.randint(0, self.size-1)
            if self.env.is_accessible(self.x, self.y):
                break
        self.visited = set() #jate loop na hoy tai nilam
        self.visited.add((self.x, self.y))
        self.accessibility_checks = 0
        self.biohazard_checks = 0
        self.movement_actions = 0
        self.cleaning_actions = 0
        self.human_encountered = 0
        self.nearest_path_selected = 0
        self.path_avoided = 0
        self.collected_objects = []
        self.move_history = []

        self.perceive() 

    def perceive(self):
        self.biohazard_checks+= 1
        if self.env.has_bio_hazard(self.x, self.y):
            self.collect()

    def collect(self):
        self.collected_objects.append((self.x, self.y))
        self.env.grid[self.x][self.y] = 0
        self.cleaning_actions+= 1


    def can_move(self, new_x, new_y, allow_visited=False):
        self.accessibility_checks+= 1
        if not self.env.is_accessible(new_x, new_y):
            return False
        if not allow_visited and (new_x, new_y) in self.visited:
            return False
        return True


    def move(self, direction):
        delta = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0)
        }
        if direction not in delta:
            return False
        dx, dy = delta[direction]
        new_x, new_y = self.x + dx, self.y + dy
        # Try unvisited first
        if self.can_move(new_x, new_y, allow_visited=False):
            self.x, self.y = new_x, new_y
            self.visited.add((self.x, self.y))
            self.move_history.append(direction)
            self.movement_actions+= 1
            self.perceive()
            return True
        elif self.can_move(new_x, new_y, allow_visited=True):
            self.x, self.y = new_x, new_y
            self.visited.add((self.x, self.y))
            self.move_history.append(direction)
            self.movement_actions+= 1
            self.perceive()
            return True
        return False

    def random_move(self, current_step):
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        random.shuffle(directions)

        delta = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0)
        }

        for dir in directions:
            dx, dy = delta[dir]
            new_x = self.x + dx
            new_y = self.y + dy

            if self.env.is_accessible(new_x, new_y):
                if self.env.has_human(new_x, new_y):
                    self.human_encountered += 1
                    return self.move_to_nearest_object(current_step)
                if self.can_move(new_x, new_y, allow_visited=False):
                    return self.move(dir)

        for dir in directions:
            dx, dy = delta[dir]
            new_x = self.x + dx
            new_y = self.y + dy

            if self.env.is_accessible(new_x, new_y):
                if self.env.has_human(new_x, new_y):
                    self.human_encountered += 1
                    return self.move_to_nearest_object(current_step)
                if self.can_move(new_x, new_y, allow_visited=True):
                    return self.move(dir)

        return False

    def get_position(self):
        return self.x, self.y

    def get_move_history(self):
        return self.move_history

    def get_collected_objects(self):
        return self.collected_objects
    
    def move_to_nearest_object(self, current_step):
        target = None
        near_position = []
        near_position.append((self.x+1, self.y))
        near_position.append((self.x-1, self.y))
        near_position.append((self.x, self.y+1))
        near_position.append((self.x, self.y-1))
        target = None

        for (near_x, near_y) in near_position:
            if 0 <= near_x < self.size and 0 <= near_y < self.size:  # inside grid
                if self.env.has_bio_hazard(near_x, near_y):
                    target = (near_x, near_y)
        if not target: 
            random.shuffle(near_position) 
            for nx, ny in near_position:
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.can_move(nx, ny, allow_visited=True):
                        target = (nx, ny)
                        break
        tar_x, tar_y = target
        if tar_x > self.x:
            direction = "RIGHT"
        elif tar_x < self.x:
            direction = "LEFT"
        elif tar_y > self.y:
            direction = "DOWN"
        else:
            direction = "UP"

        self.nearest_path_selected += 1
        self.path_avoided+=( 1000 - current_step)
        return self.move(direction)

    def simulation_summary(self):
        total_percepts = self.accessibility_checks + self.biohazard_checks
        print("Accessibility checks:", self.accessibility_checks)
        print("BioHazard checks:", self.biohazard_checks)
        print("Total percepts:", total_percepts)
        print("Movement actions:", self.movement_actions)
        print("Cleaning actions:", self.cleaning_actions)
