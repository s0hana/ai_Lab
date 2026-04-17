import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sys_module.environment import Environment, HazzardObject, Move, Transition

def test_environment_initialization():
    env = Environment(size=50, bio_hazard_number=100)
    assert env.campus.shape == (50, 50)

def test_non_accessible_generation():
    env = Environment(size=100, bio_hazard_number=0)
    obstacles = env.get_non_accessible_positions()
    assert len(obstacles) > 0

def test_bio_hazard_generation():
    env = Environment(size=50, bio_hazard_number=200)
    hazards = env.get_bio_hazard_positions()
    assert len(hazards) == 200

def test_human_generation():
    env = Environment(size=50, bio_hazard_number=0)
    humans = env.get_human_positions()
    assert len(humans) > 0

def test_is_accessible():
    env = Environment(size=20, bio_hazard_number=0)
    assert env.is_accessible(0, 0) in [True, False]

def test_has_bio_hazard():
    env = Environment(size=20, bio_hazard_number=10)
    hazards = env.get_bio_hazard_positions()
    x, y = hazards[0]
    assert env.has_bio_hazard(x, y)

def test_has_human():
    env = Environment(size=20, bio_hazard_number=0)
    humans = env.get_human_positions()
    x, y = humans[0]
    assert env.has_human(x, y)

def test_set_and_get_cell_value():
    env = Environment(size=10, bio_hazard_number=0)
    env.set_cell_value(1, 1, HazzardObject.bio_hazard)
    assert env.get_cell_value(1, 1) == HazzardObject.bio_hazard

def test_get_accessible_positions():
    env = Environment(size=20, bio_hazard_number=0)
    accessible = env.get_accessible_positions()
    assert len(accessible) > 0

def test_move_direction_vector():
    vector = Move.get_direction_vector("RIGHT")
    assert vector == (1, 0)

def test_get_all_directions():
    directions = Move.get_all_directions()
    assert len(directions) == 4

def test_transition_save_sequence():
    t = Transition()
    t.save_sequence("s1", "a1", 1, "s2")
    assert len(t.get_percept_history()) == 1

def test_transition_clear_history():
    t = Transition()
    t.save_sequence("s1", "a1", 1, "s2")
    t.clear_history()
    assert len(t.get_percept_history()) == 0