import pytest
from environment import Environment
from action_perception import Robot
from performance import Performance

class TestPerformance:

    @pytest.fixture
    def small_env(self):
        env = Environment(size=10, bio_hazard_number=5)
        return env

    @pytest.fixture
    def robot(self, small_env):
        return Robot(small_env)

    @pytest.fixture
    def performance(self, robot):
        return Performance(robot)

    def test_performance_initialization(self, performance, robot):
        assert performance.robot == robot

    def test_total_collected(self, performance, robot):
        initial_count = performance.total_collected()
        robot.collected_objects.append((1, 1))
        robot.collected_objects.append((2, 2))
        assert performance.total_collected() == initial_count + 2

    def test_total_moves(self, performance, robot):
        initial_moves = performance.total_moves()
        robot.move_history.append("UP")
        robot.move_history.append("DOWN")
        assert performance.total_moves() == initial_moves + 2

    def test_efficiency_calculation(self, performance, robot):
        robot.collected_objects = [(1, 1), (2, 2)]  # 2 collections
        robot.move_history = ["UP", "DOWN", "LEFT"]  # 3 moves
        assert performance.efficiency() == 2/3

    def test_efficiency_zero_moves(self, performance, robot):
        robot.move_history = []
        robot.collected_objects = [(1, 1)]
        assert performance.efficiency() == 0

    def test_summary_output(self, performance, capsys):
        performance.summary() 
        captured = capsys.readouterr()
        
        assert "---- Robot Performance ----" in captured.out
        assert "Collected objects:" in captured.out
        assert "Total moves:" in captured.out
        assert "Total actions:" in captured.out
        assert "Efficiency (objects per move):" in captured.out