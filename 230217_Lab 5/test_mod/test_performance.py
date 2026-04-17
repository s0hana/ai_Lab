import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sys_module.performance import Performance

class DummyRobot:
    def __init__(self):
        self.collected_objects = [1, 2, 3]
        self.movement_actions = 10
        self.cleaning_actions = 5
        self.biohazard_checks = 3
        self.accessibility_checks = 2
        self.environment = DummyEnvironment()

class DummyEnvironment:
    def get_human_positions(self):
        return [(1, 1), (2, 2)]

    def get_accessible_positions(self):
        return [(i, i) for i in range(10)]

def test_efficiency_calculation(capsys):
    robot = DummyRobot()
    perf = Performance(robot)
    perf.calculate()
    captured = capsys.readouterr()
    assert "Efficiency" in captured.out

def test_collected_objects_output(capsys):
    robot = DummyRobot()
    perf = Performance(robot)
    perf.calculate()
    captured = capsys.readouterr()
    assert "Collected objects: 3" in captured.out

def test_total_actions_output(capsys):
    robot = DummyRobot()
    perf = Performance(robot)
    perf.calculate()
    captured = capsys.readouterr()
    assert "Total actions: 20" in captured.out

def test_total_moves_output(capsys):
    robot = DummyRobot()
    perf = Performance(robot)
    perf.calculate()
    captured = capsys.readouterr()
    assert "Total moves: 10" in captured.out

def test_human_percentage_output(capsys):
    robot = DummyRobot()
    perf = Performance(robot)
    perf.calculate()
    captured = capsys.readouterr()
    assert "Human percentage" in captured.out

def test_zero_movement_efficiency(capsys):
    robot = DummyRobot()
    robot.movement_actions = 0
    perf = Performance(robot)
    perf.calculate()
    captured = capsys.readouterr()
    assert "0.0000%" in captured.out