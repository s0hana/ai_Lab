from environment import Environment
from action_perception import Robot
from performance import Performance

def main():
    env = Environment(size=100, bio_hazard_number=5000)
    robot = Robot(env)
    perf = Performance(robot)
    print("Starting robot simulation...")
    print("Initial position:", robot.get_position())
    move_limit = 1000  # number of moves to simulate
    for step in range(move_limit):
        move_dir = robot.random_move()
        if move_dir:
            print(f"Step {step+1}: Moved to {robot.get_position()}")
        else:
            print(f"Step {step+1}: Robot cannot move anywhere!")
            break  # stop if robot is stuck
    env.show_environment()
    print()
    print("\nMove history:")
    move_history = robot.get_move_history()
    if move_history:
        print(" -> ".join(move_history))
    else:
        print("No moves made.")
    perf.summary()
    
    print("Collected objects:", robot.get_collected_objects())
    print("Final position:", robot.get_position())
    robot.simulation_summary()

if __name__ == "__main__":
    main()
