import pytest
from environment import Environment

class TestEnvironment:

    @pytest.fixture
    def default_env(self):
        return Environment(size=100, bio_hazard_number=5000)

    @pytest.fixture
    def small_env(self):
        return Environment(size=10, bio_hazard_number=5)

    def test_environment_initialization(self, default_env):
        assert default_env.size == 100
        assert default_env.bio_hazard_number == 5000
        assert len(default_env.grid) == 100
        assert len(default_env.grid[0]) == 100
        assert isinstance(default_env.non_accessible_info, dict)
        assert isinstance(default_env.non_accessible, list)
        assert isinstance(default_env.bio_hazard, list)

    def test_non_accessible_area_generation(self, default_env):
        for area in default_env.non_accessible:
            for x, y in area:
                assert default_env.grid[x][y] == -1

    def test_bio_hazard_generation(self, small_env):
        assert len(small_env.bio_hazard) == 5
        for x, y in small_env.bio_hazard:
            assert small_env.grid[x][y] == 1
            assert small_env.is_accessible(x, y)  

    @pytest.mark.parametrize("x,y,expected", [
        (0, 0, True),  # Assuming (0,0) is accessible
        (2, 3, False),  # This is a non-accessible area
        (50, 50, True),  # Random accessible position
        (-1, 0, False),  # Out of bounds
        (100, 100, False),  # Out of bounds
    ])
    def test_is_accessible(self, default_env, x, y, expected):
        assert default_env.is_accessible(x, y) == expected

    def test_has_bio_hazard(self, small_env):
        if small_env.bio_hazard:
            x, y = small_env.bio_hazard[0]
            assert small_env.has_bio_hazard(x, y) == True
        for i in range(small_env.size):
            for j in range(small_env.size):
                if small_env.grid[i][j] == 0:
                    assert small_env.has_bio_hazard(i, j) == False
                   

    def test_non_accessible_boundaries(self):
        env = Environment(size=50, bio_hazard_number=100)
        for area in env.non_accessible:
            for x, y in area:
                assert 0 <= x < 50
                assert 0 <= y < 50

    def test_show_environment(self, small_env, capsys):
        small_env.show_environment()
        captured = capsys.readouterr()
        assert "Accessible co-ordinates:" in captured.out
        assert "Non-accessible co-ordinates:" in captured.out
        assert "Co-ordinates of Bio-Hazards:" in captured.out

    def test_bio_hazard_avoids_non_accessible(self, default_env):
        for x, y in default_env.bio_hazard:
            assert default_env.grid[x][y] != -1
            assert (x, y) not in [coord for area in default_env.non_accessible for coord in area]