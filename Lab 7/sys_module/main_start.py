import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from robo_sys import Robot
from performance import Performance
from sys_module.environment import Environment

def main():
    total_runs = 20
    steps_per_run = 5000
    
    all_collected = []
    all_moves = []
    all_human_encounters = []
    
    print(f"--- Starting {total_runs} Runs with Statistical Learning Agent ---")

    for i in range(total_runs):
        print(f"\n>>> Run {i+1} is starting...")
        
        env = Environment() 
        
        robot = Robot()
        robot.environment = env 
        
        robot.drive(steps_per_run)
        
        collected = len(robot.collected_objects)
        moves = robot.movement_actions
        humans = robot.human_encountered
        
        all_collected.append(collected)
        all_moves.append(moves)
        all_human_encounters.append(humans)
        
        print(f"Run {i+1} Result: Collected: {collected}, Moves: {moves}, Humans: {humans}")

    print("\n" + "="*40)
    print("      OVERALL PERFORMANCE REPORT")
    print("="*40)
    
    avg_collected = np.mean(all_collected)
    avg_moves = np.mean(all_moves)
    total_efficiency = (sum(all_collected) / sum(all_moves)) * 100 if sum(all_moves) > 0 else 0
    
    print(f"Total Runs: {total_runs}")
    print(f"Total Objects Collected: {sum(all_collected)}")
    print(f"Average Objects per Run: {avg_collected:.2f}")
    print(f"Average Moves per Run: {avg_moves:.2f}")
    print(f"Total Human Encounters: {sum(all_human_encounters)}")
    print(f"Overall Efficiency (Success Rate): {total_efficiency:.4f}%")
    print("="*40)

    #from animation.animation import RobotVisualizer
    #visualizer = RobotVisualizer(robot)
    #visualizer.animate()

if __name__ == "__main__":
    main()