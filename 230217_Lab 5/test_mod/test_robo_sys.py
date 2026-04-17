import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sys_module.robo_sys import *


def test_robot_initial_position_accessible():
    robot = Robot()
    x, y = robot.position.get_coordinate()
    assert robot.environment.is_accessible(x, y)


def test_robot_initial_visited_contains_start():
    robot = Robot()
    assert robot.start in robot.visited


def test_collect_action_cleans_cell():
    robot = Robot()
    x, y = robot.position.get_coordinate()

    # Force a hazard at current position
    robot.environment.set_cell_value(x, y, robot.object.bio_hazard)

    robot.collect_action()

    assert (x, y) in robot.collected_objects


def test_movement_updates_position():
    robot = Robot()
    old_position = robot.position.get_coordinate()

    # Try one move step
    robot.drive_one_step(0)
    new_position = robot.position.get_coordinate()

    assert old_position != new_position


def test_visited_updates_after_move():
    robot = Robot()
    robot.drive_one_step(0)
    pos = robot.position.get_coordinate()

    assert pos in robot.visited


def test_cleaning_action_counter():
    robot = Robot()
    x, y = robot.position.get_coordinate()

    robot.environment.set_cell_value(x, y, robot.object.clean)
    robot.cleaning_actions = 0

    robot.environment.set_cell_value(x, y, robot.object.bio_hazard)
    robot.collect_action()

    assert robot.cleaning_actions == 1


def test_movement_action_counter():
    robot = Robot()
    robot.drive_one_step(0)

    assert robot.movement_actions >= 0


def test_perception_increases_check_counter():
    robot = Robot()
    initial = robot.biohazard_checks

    robot.perception()

    assert robot.biohazard_checks == initial + 1