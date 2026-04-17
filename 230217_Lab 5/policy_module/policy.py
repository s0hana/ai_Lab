import random
from sys_module.environment import Move

class Policy:
    def __init__(self):
        pass

    @staticmethod
    def getRandomMove():
        return random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

    def obstacle_avoidance(self, robot):
        """Find next move avoiding obstacles"""
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        random.shuffle(directions)

        delta = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0)
        }

        # Try unvisited cells first
        for d in directions:
            dx, dy = delta[d]
            nx, ny = robot.position.x + dx, robot.position.y + dy

            if robot.can_move(nx, ny, allow_visited=False):
                return d

        # Try visited cells if no unvisited available
        for d in directions:
            dx, dy = delta[d]
            nx, ny = robot.position.x + dx, robot.position.y + dy

            if robot.can_move(nx, ny, allow_visited=True):
                return d

        return None

    def shortest_path(self, robot, current_step):
        """Find path to nearest hazard"""
        near = [
            (robot.position.x + 1, robot.position.y),
            (robot.position.x - 1, robot.position.y),
            (robot.position.x, robot.position.y + 1),
            (robot.position.x, robot.position.y - 1)
        ]

        target = None

        # Look for hazard in adjacent cells
        for nx, ny in near:
            if 0 <= nx < robot.size and 0 <= ny < robot.size:
                if robot.environment.has_bio_hazard(nx, ny):
                    target = (nx, ny)
                    break

        # If no hazard found, find any accessible cell
        if not target:
            random.shuffle(near)
            for nx, ny in near:
                if 0 <= nx < robot.size and 0 <= ny < robot.size:
                    if robot.can_move(nx, ny, allow_visited=True):
                        target = (nx, ny)
                        break

        if not target:
            return None

        tx, ty = target
        
        # Determine direction to target
        if tx > robot.position.x:
            return "RIGHT"
        elif tx < robot.position.x:
            return "LEFT"
        elif ty > robot.position.y:
            return "DOWN"
        else:
            return "UP"

    def get_action(self, robot, current_step):
        """Main decision-making method"""
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        delta = {
            "UP": (0, 1),
            "DOWN": (0, -1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0)
        }

        # Check for humans in adjacent cells
        for d in directions:
            dx, dy = delta[d]
            nx, ny = robot.position.x + dx, robot.position.y + dy

            if robot.environment.is_accessible(nx, ny):
                if robot.environment.has_human(nx, ny):
                    robot.human_encountered += 1
                    return self.shortest_path(robot, current_step)

        # Try to go to nearest hazard
        action = self.shortest_path(robot, current_step)
        if action:
            return action

        # Try obstacle avoidance
        action = self.obstacle_avoidance(robot)
        if action:
            return action

        # Default to random move
        return self.getRandomMove()