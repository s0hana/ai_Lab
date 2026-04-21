import random
from sys_module.environment import Move
import numpy as np
import os

class Policy:
    def __init__(self):
        try:
            self.p_map = np.load(r"D:\3-2\Artificial Intelligence\Lab\Lab 7\random configuration\probability_map.npy")
            self.threshold = 0.5  
        except:
            self.p_map = None
            self.threshold = 0.5

    @staticmethod
    def getRandomMove():
        return random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
#function which uses threshold
    def statistical_move(self, robot):
        if self.p_map is None:
            return None

        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        delta = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0)
        }

        best_move = None
        max_prob = -1

        for d in directions:
            dx, dy = delta[d]
            nx, ny = robot.position.x + dx, robot.position.y + dy

            if 0 <= nx < 100 and 0 <= ny < 200:
                current_p = self.p_map[nx, ny]
                if current_p >= self.threshold and current_p > max_prob:
                    if robot.can_move(nx, ny, allow_visited=True):
                        max_prob = current_p
                        best_move = d
        
        return best_move

    def obstacle_avoidance(self, robot):
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        random.shuffle(directions)
        delta = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}

        for d in directions:
            dx, dy = delta[d]
            nx, ny = robot.position.x + dx, robot.position.y + dy
            if robot.can_move(nx, ny, allow_visited=False):
                return d
        for d in directions:
            dx, dy = delta[d]
            nx, ny = robot.position.x + dx, robot.position.y + dy
            if robot.can_move(nx, ny, allow_visited=True):
                return d
        return None

    def shortest_path(self, robot, current_step):
        hi = getattr(robot, 'hi', 100) 
        wd = getattr(robot, 'wd', 100)

        near = [
            (robot.position.x + 1, robot.position.y),
            (robot.position.x - 1, robot.position.y),
            (robot.position.x, robot.position.y + 1),
            (robot.position.x, robot.position.y - 1)
        ]

        target = None
        for nx, ny in near:
            if 0 <= nx < hi and 0 <= ny < wd:
                if robot.environment.has_bio_hazard(nx, ny):
                    target = (nx, ny)
                    break

        if not target:
            return None

        tx, ty = target
        if tx > robot.position.x: return "RIGHT"
        elif tx < robot.position.x: return "LEFT"
        elif ty > robot.position.y: return "DOWN"
        else: return "UP"

    def get_action(self, robot, current_step):
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        delta = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}

        for d in directions:
            dx, dy = delta[d]
            nx, ny = robot.position.x + dx, robot.position.y + dy
            if 0 <= nx < 100 and 0 <= ny < 100:
                if robot.environment.is_accessible(nx, ny):
                    if robot.environment.has_human(nx, ny):
                        robot.human_encountered += 1
                        return self.obstacle_avoidance(robot)

        action = self.shortest_path(robot, current_step)
        if action:
            return action

        action = self.statistical_move(robot)
        if action:
            return action

        action = self.obstacle_avoidance(robot)
        if action:
            return action

        return self.getRandomMove()