import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sys_module.robo_sys import Robot
from animation import RobotVisualizer

def main():
    robot = Robot()
    visualizer = RobotVisualizer(robot)
    visualizer.animate()

if __name__ == "__main__":
    main()