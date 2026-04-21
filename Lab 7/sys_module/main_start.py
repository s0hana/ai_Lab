import sys
import os
import numpy as np
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from robo_sys import Robot
from performance import *
from sys_module.environment import Environment
from random_configuration.generate_data import *


def main():
    save_configurations()
    calculate_probability_map()
    total_runs = 20
    steps_per_run = 2000


    all_collected = []
    all_moves = []
    all_human_encounters = []

    print(f"--- Starting {total_runs} Runs using Saved Configurations ---")

    for i in range(total_runs):
        print(f"\n>>> Run {i+1} is starting...")

        env = Environment()

        robot = Robot()
        robot.environment = env

        robot.drive(steps_per_run)

        perf = Performance(robot)
        perf.calculate()

        folder = Path(r"D:\3-2\Artificial Intelligence\Lab\Lab 7\output_environments_new_20_run")
        folder.mkdir(exist_ok=True)
        file_path = folder / f"result{i+1}.txt"
        with open(file_path, "w") as file:
            file.write(f"This is output of run {i+1}: Move history: {robot.move_history}")
            file.write("Environment Grid:\n")
    
            for row in robot.environment.campus:
                for item in row:
                    file.write(str(item) + " ")
                file.write("\n")

        collected = len(robot.collected_objects)
        moves = robot.movement_actions
        humans = robot.human_encountered

        all_collected.append(collected)
        all_moves.append(moves)
        all_human_encounters.append(humans)

        print(f"Run {i+1} Result: Collected: {collected}, Moves: {moves}, Humans Encounters: {humans}")

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
    print(f"Error Rate: {100 - total_efficiency: .4f}%")
    print("="*40)


if __name__ == "__main__":
    main()