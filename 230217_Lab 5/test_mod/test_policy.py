import sys
import pytest
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from policy_module.policy import *  

class DummyEnvironment:
    def __init__(self, hazards=None, humans=None):
        self.hazards = hazards or []
        self.humans = humans or []

    def has_bio_hazard(self, x, y):
        return (x, y) in self.hazards

    def has_human(self, x, y):
        return (x, y) in self.humans

    def is_accessible(self, x, y):
        return True  

class DummyPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class DummyRobot:
    def __init__(self, x=0, y=0, size=5, env=None):
        self.position = DummyPosition(x, y)
        self.size = size
        self.environment = env or DummyEnvironment()
        self.visited = set()
        self.human_encountered = 0

    def can_move(self, x, y, allow_visited=True):
        if 0 <= x < self.size and 0 <= y < self.size:
            if not allow_visited and (x, y) in self.visited:
                return False
            return True
        return False

@pytest.fixture
def policy():
    return Policy()

@pytest.fixture
def robot():
    env = DummyEnvironment(hazards=[(1, 0)], humans=[(0, 1)])
    return DummyRobot(x=0, y=0, size=5, env=env)

def test_get_random_move(policy):
    move = policy.getRandomMove()
    assert move in ["UP", "DOWN", "LEFT", "RIGHT"]

def test_obstacle_avoidance_unvisited(policy):
    robot = DummyRobot(x=2, y=2, size=5)
    move = policy.obstacle_avoidance(robot)
    assert move in ["UP", "DOWN", "LEFT", "RIGHT"]

def test_obstacle_avoidance_visited(policy):
    robot = DummyRobot(x=2, y=2, size=5)
    robot.visited = {(2,3),(2,1),(1,2),(3,2)}
    move = policy.obstacle_avoidance(robot)
    assert move in ["UP", "DOWN", "LEFT", "RIGHT"]

def test_shortest_path_to_hazard(policy):
    robot = DummyRobot(x=0, y=0, size=5, env=DummyEnvironment(hazards=[(1,0)]))
    move = policy.shortest_path(robot, current_step=0)
    assert move == "RIGHT"

def test_shortest_path_no_hazard(policy):
    robot = DummyRobot(x=0, y=0, size=5)
    move = policy.shortest_path(robot, current_step=0)
    assert move in ["UP", "DOWN", "LEFT", "RIGHT"]

def test_get_action_human_nearby(policy):
    robot = DummyRobot(x=0, y=0, size=5, env=DummyEnvironment(hazards=[(1,0)], humans=[(0,1)]))
    move = policy.get_action(robot, current_step=0)
    assert move == "RIGHT"  

def test_get_action_default_move(policy):
    robot = DummyRobot(x=0, y=0, size=5)
    move = policy.get_action(robot, current_step=0)
    assert move in ["UP", "DOWN", "LEFT", "RIGHT"]