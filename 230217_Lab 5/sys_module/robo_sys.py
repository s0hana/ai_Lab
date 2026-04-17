import random 
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sys_module.environment import *
from policy_module.policy import *

class coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def update(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
    def get_coordinate(self):
        return (self.x, self.y)
class Robot:
    def __init__(self):
        self.environment = Environment()
        self.transition = Transition()
        self.object = HazzardObject()
        self.policy = Policy()

        self.size = self.environment.size

        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.environment.is_accessible(x, y):
                break
        self.position = coordinate(x, y)
        self.start = (x, y)
        self.visited = set()
        self.visited.add((x, y))

        self.accessibility_checks = 0
        self.biohazard_checks = 0
        self.movement_actions = 0
        self.cleaning_actions = 0
        self.human_encountered = 0

        self.move_history = []
        self.collected_objects = []

        self.perception()
        
    def perception(self):
        self.biohazard_checks+=1
        x, y = self.position.get_coordinate()
        if self.environment.has_bio_hazard(x, y):
            self.collect_action()

    def collect_action(self):
        x, y = self.position.get_coordinate()

        self.collected_objects.append((x, y))
        self.environment.set_cell_value(x, y, HazzardObject.clean)

        self.cleaning_actions+=1

    def initiate_human(self):
        self.environment.generate_humans()

    def initiate_hazard(self):
        self.environment.generate_bio_hazard()

    def drive(self, steps):
        for step in range(steps):
            self.drive_one_step(step)

    def drive_one_step(self, current_step):
        action = self.policy.get_action(self, current_step)
        if action is None:
            return False
        
        self.update_position(action)
        return True
    
    def can_move(self, new_x, new_y, allow_visited = False):
        self.accessibility_checks+=1

        if not self.environment.is_accessible(new_x, new_y):
            return False
        if not allow_visited and (new_x, new_y) in self.visited:
            return False
        return True
    
    def update_position(self, action):
        x, y = Move.get_direction_vector(action)
        new_x = self.position.x + x
        new_y = self.position.y + y

        if self.can_move(new_x, new_y, allow_visited=False):
            pass
        elif self.can_move(new_x, new_y, allow_visited=True):
            pass
        else:
            return False
        
        self.position.update(new_x, new_y)
        self.visited.add((new_x, new_y))

        self.move_history.append(action)
        self.movement_actions+=1

        self.perception()

        return True


    def display_env(self):
        self.environment.display_env()