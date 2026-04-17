import pytest
from environment import Environment
from action_perception import Robot
from performance import Performance

class TestIntegration:
    @pytest.fixture
    def small_env(self):
        return Environment(size=10, bio_hazard_number=5)

    @pytest.fixture
    def robot(self, small_env):
        return Robot(small_env)

    @pytest.fixture
    def performance(self, robot):
        return Performance(robot)

    def test_full_simulation(self, robot, performance):
        move_limit = 50
        collected_before = performance.total_collected()
        moves_before = performance.total_moves()
        for _ in range(move_limit):
            moved = robot.random_move(100)
            if moved is None:  
                break
        assert performance.total_moves() >= moves_before
        assert performance.total_collected() >= collected_before
        eff = performance.efficiency()
        assert 0 <= eff <= 1

    def test_robot_respects_boundaries(self, robot):
        for _ in range(100):
            robot.random_move(100)
            x, y = robot.get_position()
            assert robot.env.is_accessible(x, y)

    def test_collected_objects_cleared(self, robot):
        x, y = robot.get_position()
        robot.env.grid[x][y] = 1
        robot.env.bio_hazard.append((x, y))
        robot.perceive()
        assert (x, y) in robot.get_collected_objects()
        assert robot.env.grid[x][y] == 0

    def test_performance_summary(self, robot, performance, capsys):
        for _ in range(10):
            robot.random_move(100)
        performance.summary()
        captured = capsys.readouterr()
        assert "Collected objects:" in captured.out
        assert "Total moves:" in captured.out
        assert "Efficiency (objects per move):" in captured.out
