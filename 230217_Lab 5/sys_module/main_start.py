import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from animation.animation import *
from robo_sys import *
from performance import *
def main():
    robot = Robot()
    #robot.initiate_human()
    #robot.initiate_hazard()
    print("Starting Simulation: ")
    steps = 2000
    robot.drive(steps)
    print("Simulation is done!")
    print(f"Move History: {robot.move_history}")
    print(f"Environment: ")
    robot.display_env()
    print(f"Starting position: {robot.start}")
    print(f"Final Position: {robot.position.get_coordinate()}")
    print(f"Visited Cells: {len(robot.visited)}")
    print(f"Collected Objects: {len(robot.collected_objects)}")
    print(f"Movement Actions: {robot.movement_actions}")
    print(f"Cleaning Actions: {robot.cleaning_actions}")
    print(f"Human Encounters: {robot.human_encountered}")
    print(f"Accessibility Cahecks: {robot.accessibility_checks}")
    print(f"Biohazard Checks: {robot.biohazard_checks}")
    perf = Performance(robot)
    perf.calculate()
    visualizer = RobotVisualizer(robot)
    #visualizer.animate()
if __name__ == "__main__":
    main()