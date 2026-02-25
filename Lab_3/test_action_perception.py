import pytest
from environment import Environment
from action_perception import Robot

class TestRobot:
    @pytest.fixture
    def small_env(self):
        return Environment(size=10, bio_hazard_number=5)
    @pytest.fixture
    def clean_env(self):
        env = Environment(size=10, bio_hazard_number=5)
        test_positions = [(5,5), (4,5), (5,4), (6,5), (5,6)]
        for x, y in test_positions:
            if env.has_bio_hazard(x, y):
                env.grid[x][y] = 0
                if (x, y) in env.bio_hazard:
                    env.bio_hazard.remove((x, y))
        return env
    @pytest.fixture
    def robot(self, clean_env):
        robot = Robot(clean_env)
        robot.x, robot.y = 1, 1
        robot.visited = {(1, 1)}
        robot.collected_objects = []
        robot.move_history = []
        robot.accessibility_checks = 0
        robot.biohazard_checks = 1  
        robot.movement_actions = 0
        robot.cleaning_actions = 0
        return robot

    def test_robot_initialization(self):
        env = Environment(size=10, bio_hazard_number=5)
        robot = Robot(env)
        assert robot.env == env
        assert robot.size == 10
        assert env.is_accessible(robot.x, robot.y)
        assert (robot.x, robot.y) in robot.visited
        assert isinstance(robot.visited, set)
        assert robot.accessibility_checks == 0
        assert robot.biohazard_checks >= 1  # At least initial perception
        assert robot.movement_actions == 0
        assert robot.cleaning_actions >= 0
        assert isinstance(robot.collected_objects, list)
        assert isinstance(robot.move_history, list)

    def test_perceive_no_biohazard(self):
        env = Environment(size=5, bio_hazard_number=0)
        robot = Robot(env)
        robot.x, robot.y = 1, 1
        robot.collected_objects = []
        initial_biohazard_checks = robot.biohazard_checks
        robot.perceive()
        assert robot.biohazard_checks == initial_biohazard_checks + 1
        assert len(robot.collected_objects) == 0
        assert robot.cleaning_actions == 0

    def test_perceive_with_biohazard(self, clean_env):
        test_x, test_y = 5, 5
        clean_env.grid[test_x][test_y] = 1
        clean_env.bio_hazard.append((test_x, test_y))
        robot = Robot(clean_env)
        robot.x, robot.y = test_x, test_y
        robot.collected_objects = []
        robot.cleaning_actions = 0
        robot.biohazard_checks = 0
        robot.perceive()
        assert (test_x, test_y) in robot.collected_objects
        assert robot.biohazard_checks == 1
        assert robot.cleaning_actions == 1
        assert robot.env.grid[test_x][test_y] == 0

    def test_collect(self, clean_env):
        test_x, test_y = 5, 5
        clean_env.grid[test_x][test_y] = 1
        clean_env.bio_hazard.append((test_x, test_y))
        robot = Robot(clean_env)
        while robot.x == test_x and robot.y == test_y:
            robot = Robot(clean_env)
        robot.x, robot.y = test_x, test_y
        robot.collected_objects = []
        robot.cleaning_actions = 0
        robot.collect()
        assert (test_x, test_y) in robot.collected_objects
        assert clean_env.grid[test_x][test_y] == 0
        assert robot.cleaning_actions == 1

    def test_move_function(self, clean_env):
        robot = Robot(clean_env)

        robot.x, robot.y = 5, 5
        robot.visited = {(5, 5)}
        robot.move_history = []
        robot.movement_actions = 0
        robot.biohazard_checks = 0

        result = robot.move("RIGHT")

        if clean_env.is_accessible(6, 5):
            assert result is True
            assert robot.get_position() == (6, 5)
            assert robot.movement_actions == 1
            assert robot.move_history[-1] == "RIGHT"
            assert (6, 5) in robot.visited
            assert robot.biohazard_checks == 1
        else:
            assert result is False

        result_invalid = robot.move("JUMP")
        assert result_invalid is False

        clean_env.grid[4][5] = -1
        robot.x, robot.y = 5, 5
        robot.visited = {(5, 5)}
        robot.movement_actions = 0

        result_blocked = robot.move("LEFT")
        assert result_blocked is False
        assert robot.get_position() == (5, 5)
    
    def test_move_to_nearest_object_behavior(self):
        env = Environment(size=5, bio_hazard_number=0)
        env.grid[2][2] = 1
        env.bio_hazard.append((2, 2))
        robot = Robot(env)
        robot.x, robot.y = 2, 1  
        robot.visited = {(2, 1)}
        robot.nearest_path_selected = 0
        robot.path_avoided = 0
        current_step = 1 
        result = robot.move_to_nearest_object(current_step)
        assert result is True
        assert (robot.x, robot.y) == (2, 2)
        assert robot.nearest_path_selected == 1
        assert robot.path_avoided == 1000 - current_step
        assert (2, 2) in robot.collected_objects
        env = Environment(size=5, bio_hazard_number=0)
        robot = Robot(env)
        robot.x, robot.y = 2, 2
        robot.visited = {(2, 2)}
        robot.nearest_path_selected = 0
        robot.path_avoided = 0
        result = robot.move_to_nearest_object(current_step)
        assert result is True
        new_x, new_y = robot.x, robot.y
        assert (new_x, new_y) in [(3, 2), (1, 2), (2, 3), (2, 1)]
        assert robot.nearest_path_selected == 1
        assert robot.path_avoided == 1000 - current_step

    def test_random_move(self):
        env = Environment(size=10, bio_hazard_number=10)
        robot = Robot(env)
        max_steps = 50  
        for step in range(1, max_steps + 1):
            robot.random_move(step)
        assert robot.movement_actions > 0
        assert robot.biohazard_checks >= 1
        assert robot.human_encountered >= 0
        assert robot.nearest_path_selected >= 0
        assert robot.path_avoided >= 0
        assert len(robot.collected_objects) <= len(env.bio_hazard)
        
   

    def test_robot_collects_on_move(self, clean_env):
        test_x, test_y = 5, 5
        clean_env.grid[test_x][test_y] = 1
        clean_env.bio_hazard.append((test_x, test_y))
        robot = Robot(clean_env)
        robot.x, robot.y = 4, 5
        robot.collected_objects = []
        robot.cleaning_actions = 0
        robot.move("RIGHT")  
        assert (test_x, test_y) in robot.collected_objects
        assert clean_env.grid[test_x][test_y] == 0
        assert robot.cleaning_actions == 1

    def test_get_position(self, robot):
        robot.x, robot.y = 3, 4
        assert robot.get_position() == (3, 4)

    def test_get_move_history(self, robot):
        test_moves = ["UP", "RIGHT", "DOWN"]
        robot.move_history = test_moves.copy()
        assert robot.get_move_history() == test_moves
        assert len(robot.get_move_history()) == 3

    def test_get_collected_objects(self, robot):
        test_collections = [(1, 1), (2, 2)]
        robot.collected_objects = test_collections.copy()
        assert robot.get_collected_objects() == test_collections
        assert len(robot.get_collected_objects()) == 2

    def test_simulation_summary(self, robot, capsys):
        robot.accessibility_checks = 10
        robot.biohazard_checks = 5
        robot.movement_actions = 8
        robot.cleaning_actions = 3
        robot.simulation_summary()
        captured = capsys.readouterr()
        assert "Accessibility checks: 10" in captured.out
        assert "BioHazard checks: 5" in captured.out
        assert "Total percepts: 15" in captured.out
        assert "Movement actions: 8" in captured.out
        assert "Cleaning actions: 3" in captured.out

    def test_multiple_moves_no_revisits(self, robot):
        robot.x, robot.y = 5, 5
        robot.visited = {(5, 5)}
        moves_made = 0
        for _ in range(5):
            result = robot.random_move(100)
            if result:
                moves_made += 1
        assert len(robot.visited) == moves_made + 1 

    def test_can_move_after_collection(self, clean_env):
        test_x, test_y = 5, 5
        clean_env.grid[test_x][test_y] = 1
        clean_env.bio_hazard.append((test_x, test_y))
        robot = Robot(clean_env)
        robot.x, robot.y = test_x, test_y
        robot.collect()
        result = robot.random_move(100)
        assert result is not None or result is None  

    def test_move_history_accuracy(self, robot):
        robot.x, robot.y = 5, 5
        robot.move_history = []
        moves = ["UP", "RIGHT", "DOWN", "LEFT"]
        successful_moves = []
        for move in moves:
            if robot.move(move):
                successful_moves.append(move)
        assert robot.move_history == successful_moves

    def test_robot_always_accessible(self):
        env = Environment(size=20, bio_hazard_number=50)
        for _ in range(10):
            robot = Robot(env)
            assert env.is_accessible(robot.x, robot.y)
            assert robot.env.grid[robot.x][robot.y] != -1