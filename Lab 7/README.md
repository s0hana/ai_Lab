# Bio-Hazard Cleanup Robot Simulation

This project simulates an autonomous robot navigating a **100×100 grid campus environment**. The robot's goal is to efficiently locate and collect bio-hazardous materials while avoiding static obstacles and dynamic human entities.

---
## Lab Task Overview

This simulation fulfills the following requirements:

### Mass Configuration Generation
- Generated **100 random campus configurations** (minimum size: 80×100).
- Each configuration includes varied placements of:
  - Bio-hazards
  - Humans
  - Non-accessible obstacles

### Persistence
- All configurations are saved as `.npy` files in `random_configuration/configs` folder.
- Stored in a dedicated directory for reproducibility.

### Statistical Analysis
- Built a **probability map (`p_map`)** from the 100 configurations by using `calculate_probability_map()` function in `generate_data.py`.
- Guides the robot toward regions with historically high hazard density.

###  Batch Execution
- Conducted **20 independent simulation runs**.
- Each run consists of **2000 steps**.
- Used saved configurations and probability map for evaluation.

---

##  System Architecture

### 1. Environment & Objects (`environment.py`)
- Defines grid entities:
  - `-1` → Non-accessible areas
  - `1` → Bio-hazards
  - `2` → Humans
- Random placement logic:
  - Humans: 15–25% density
  - Hazards: randomly distributed in accessible areas
- Maintains **state-action transition history** for analysis.

---

### 2. Robot Brain (`robo_sys.py` & `policy.py`)

The robot follows a **hierarchical decision-making strategy**:

#### 1. Safety First
- Detects humans in adjacent cells.
- Increments encounter counter.
- Triggers `obstacle_avoidance`.

#### 2. Greedy Cleanup
- Prioritizes nearby hazards.
- Uses `shortest_path` to collect immediately reachable hazards.

#### 3. Statistical Navigation
- Uses `probability_map.npy`.
- Moves toward neighbors with probability >= threshold (e.g., 0.5).

#### 4. Reactive Avoidance
- Avoids obstacles dynamically.
- Prefers unvisited cells to improve exploration.

---

### 3. Data & Performance

#### `generate_data.py`
- Generates:
  - 100 environment configurations saved in `configs` folder
  - Probability heatmap (`p_map`)

#### `performance.py`
Calculates:
- Efficiency (objects collected per move)
- Total actions
- Human encounter rate

---

## How to Run

### Run python main_start.py
Outputs:
- Performance reports
- Move history logs
- Move histories and grids are saved in: `output_environments_new_20_run/`