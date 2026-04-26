import numpy as np
import random

class HazzardObject:
    accessible = 0        
    non_accessible = -1  
    bio_hazard = 1        
    human = 2             
    clean = 0             
    
    def __init__(self):
        pass

class Environment:
    def __init__(self, hi=80, wd=100, bio_hazard_number=2000):
        self.hi = hi
        self.wd = wd
        self.bio_hazard_number = bio_hazard_number
        self.campus = np.zeros((self.hi, self.wd), dtype=int)
        
        self.non_accessible_info = {
            (2, 3): (15, 14),
            (30, 70): (7, 7),
            (10, 40): (14, 16),
            (52, 5): (12, 13),
            (45, 57): (12, 15)
        }
        
        self.generate_non_accessible()
        self.generate_bio_hazard()
        self.generate_humans()
    
    def generate_non_accessible_area(self, start_x, end_x, start_y, end_y):
        self.campus[start_x:end_x, start_y:end_y] = HazzardObject.non_accessible

    def load_configuration(self, config):
        self.grid = config 
        
    def generate_non_accessible(self):
        for (x, y), (h, w) in self.non_accessible_info.items():
            start_x = x
            end_x = min(x + w, self.hi)  
            start_y = y
            end_y = min(y + h, self.wd) 
            self.generate_non_accessible_area(start_x, end_x, start_y, end_y)
    
    def generate_humans(self):
        accessible_cells = []
        for i in range(self.hi):
            for j in range(self.wd):
                if self.campus[i, j] == HazzardObject.accessible:
                    accessible_cells.append((i, j))
        
        total_accessible = len(accessible_cells)
        human_count = int(total_accessible * random.uniform(0.15, 0.25))
        
        if human_count > 0:
            selected = random.sample(accessible_cells, human_count)
            for (x, y) in selected:
                self.campus[x, y] = HazzardObject.human
    
    def generate_bio_hazard(self):
        count = 0
        while count < self.bio_hazard_number:
            x = random.randint(0, self.hi - 1)
            y = random.randint(0, self.wd - 1)
            if self.campus[x, y] == HazzardObject.accessible:
                self.campus[x, y] = HazzardObject.bio_hazard
                count += 1
    
    def is_accessible(self, x, y):
        if 0 <= x < self.hi and 0 <= y < self.wd:
            return self.campus[x, y] != HazzardObject.non_accessible
        return False
    
    def has_bio_hazard(self, x, y):
        if 0 <= x < self.hi and 0 <= y < self.wd:
            return self.campus[x, y] == HazzardObject.bio_hazard
        return False
    
    def has_human(self, x, y):
        if 0 <= x < self.hi and 0 <= y < self.wd:
            return self.campus[x, y] == HazzardObject.human
        return False
    
    def get_cell_value(self, x, y):
        if 0 <= x < self.hi and 0 <= y < self.wd:
            return self.campus[x, y]
        return None
    
    def set_cell_value(self, x, y, value):
        if 0 <= x < self.hi and 0 <= y < self.wd:
            self.campus[x, y] = value
    
    def display_env(self):
        print("Environment Grid:")
        for row in self.campus:
            for item in row:
                print(item, end=" ")
            print()
    
    def get_human_positions(self):
        humans = []
        for i in range(self.hi):
            for j in range(self.wd):
                if self.campus[i, j] == HazzardObject.human:
                    humans.append((i, j))
        return humans
    
    def get_bio_hazard_positions(self):
        hazards = []
        for i in range(self.hi):
            for j in range(self.wd):
                if self.campus[i, j] == HazzardObject.bio_hazard:
                    hazards.append((i, j))
        return hazards
    
    def get_non_accessible_positions(self):
        obstacles = []
        for i in range(self.hi):
            for j in range(self.wd):
                if self.campus[i, j] == HazzardObject.non_accessible:
                    obstacles.append((i, j))
        return obstacles
    
    def get_accessible_positions(self):
        accessible = []
        for i in range(self.hi):
            for j in range(self.wd):
                if self.campus[i, j] == HazzardObject.accessible:
                    accessible.append((i, j))
        return accessible


class Move:
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    
    @staticmethod
    def get_direction_vector(direction):
        direction_map = {
            "RIGHT": Move.RIGHT,
            "LEFT": Move.LEFT,
            "UP": Move.UP,
            "DOWN": Move.DOWN
        }
        return direction_map.get(direction, (0, 0))
    
    @staticmethod
    def get_all_directions():
        return ["UP", "DOWN", "LEFT", "RIGHT"]


class Transition:
    def __init__(self):
        self.percept_history = []
    
    def get_percept_history(self):
        return self.percept_history
    
    def save_sequence(self, state, action, reward, next_state):
        self.percept_history.append({
            'state': state,
            'action': action,
            'reward': reward,
            'next_state': next_state
        })
    
    def clear_history(self):
        self.percept_history = []