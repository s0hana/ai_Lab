import numpy as np
import os
import sys
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sys_module.environment import Environment

#generate 100 configuration for probability map
def save_configurations(n=100, folder=r"D:\3-2\Artificial Intelligence\Lab\Lab 8\random_configuration\configs"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    for i in range(n):
        hi = 100
        wd = 100
        env = Environment(hi=hi, wd=wd) 
        
        file_path = os.path.join(folder, f"config_{i}.npy")
        np.save(file_path, env.campus)
        
    print(f"Successfully saved {n} configurations in '{folder}' folder.")

def calculate_probability_map(n=100, folder=r"D:\3-2\Artificial Intelligence\Lab\Lab 8\random_configuration\configs"):
    prob_map = np.zeros((100, 100))
    for i in range(n):
        file_path = os.path.join(folder, f"config_{i}.npy")
        grid = np.load(file_path)
        h, w = grid.shape
        prob_map[:h, :w] += (grid == 1).astype(int)
    prob_map = prob_map / n #this map is used in policy.py of sys_module where statistical_move decides based on threshold,( probability>=threshold)
    return prob_map

if __name__ == "__main__":
    save_configurations(100)
    p_map = calculate_probability_map() 
    np.save(r"D:\3-2\Artificial Intelligence\Lab\Lab 8\random_configuration\probability_map.npy", p_map) 
    print("probability_map.npy is generated!")