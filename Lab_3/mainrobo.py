from environment import Environment
from action_perception import Robot
from performance import Performance

def main():
    env = Environment(size=100, bio_hazard_number=5000)
    robot = Robot(env)
    perf = Performance(robot)
    print()
    print()
    print("Starting robot simulation...")
    print("Initial position:", robot.get_position())
    move_limit = 1000  # number of moves to simulate
    for step in range(move_limit):
        move_dir = robot.random_move(step+1)
        """if move_dir:
            print(f"Step {step+1}: Moved to {robot.get_position()}")
        else:
            print(f"Step {step+1}: Robot cannot move anywhere!")
            break  """# stop if robot is stuck
    #env.show_environment()
    print("Move history:")
    move_history = robot.get_move_history()
    if move_history:
        print(" -> ".join(move_history))
    else:
        print("No moves made.")
    perf.summary()
    
    print("Collected objects:", robot.get_collected_objects())
    print("Final position:", robot.get_position())
    robot.simulation_summary()
    print("Number of human encountered:", robot.human_encountered)
    print("Number of nearest path selected :", robot.nearest_path_selected)
    print("Avoided: ", robot.path_avoided)
    print("Number of object collected:", len(robot.get_collected_objects()))

if __name__ == "__main__":
        for i in range(100):
            print(f"\n\nSimulation {i+1}")
            main()
