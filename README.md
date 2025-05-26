# Deepimax: Adversarial Search Over Deep Decision Trees

This repository contains the implementation of **Deepimax**, an adversarial search algorithm over deep decision trees. Originally developed in 2016 as part of a university research article and submitted to the **IEEE Hamedan Student Branch** under code **C-IT16-09950264**, Deepimax presents a more efficient and practical alternative to classical algorithms such as **Minimax**, **Minimax with Alpha-Beta Pruning**, and **Expectimax**.

> 🚀 Repository: [alizandian/deepimax](https://github.com/alizandian/deepimax)

---

## 🧠 Overview

Deepimax is designed to improve decision-making in adversarial environments by offering:
- Better **time and space complexity**
- More **practical performance**
- A clear improvement over traditional search algorithms

A custom game implementation of **Fox and Sheeps** is used as the testing playground, developed with minimal dependencies in Python.

---

## 📦 Project Purpose

This project serves two primary goals:

1. **Implementation** of Deepimax algorithm.
2. **Benchmarking** and comparison against Minimax, MinimaxABP, and Expectimax through real-time simulation in a simplified game environment.

---

## 🛠️ Installation

The easiest way to set up the environment is with **conda**:

### Step-by-step Setup

```bash
# Create and activate conda environment
conda create --name deepimax_env python=3.7
conda activate deepimax_env

# Install required package
conda install plotly
```

### ✅ Tested Environment

Use `conda list` to confirm the following packages are installed:

```
ca-certificates           2019.11.27
certifi                   2019.11.28
openssl                   1.1.1d
pip                       20.0.2
plotly                    4.4.1
python                    3.7.6
retrying                  1.3.3
setuptools                45.1.0
six                       1.14.0
sqlite                    3.30.1
vc                        14.1
vs2015_runtime            14.16.27012
wheel                     0.33.6
wincertstore              0.2
```

shorter version:

```
plotly==4.4.1
retrying==1.3.3
six==1.14.0
certifi==2019.11.28
setuptools==45.1.0
pip==20.0.2
wheel==0.33.6
```

---

## 🚀 Running the Project

Start the project by executing:

```bash
python FoxAndSheeps.py
```

This launches the game environment UI.

---

## 🎮 Game Controls and Algorithms

### Role Selection

- `player`: Human player
- `bot`: Choose among:
  - Minimax
  - Minimax Alpha-Beta Pruning (MinimaxABP)
  - Expectimax
  - **Deepimax** (proposed)

### Algorithm Parameters

- **depth**: Controls how deep the algorithm can explore in the decision tree.
- **roa** / **doa**: Deepimax-specific parameters (range and depth of accuracy). Best left unchanged unless familiar with internals.
- **Max Moves**: Number of moves simulated per play.
- **Turn Time**: Maximum allowed time per move.

---

## ⚙️ Heuristic Parameters

Customizable through UI (modify with caution):

| Variable | Description |
|----------|-------------|
| `SM` (Sheep Separation) | Importance of sheep staying grouped |
| `SCM` (Sheep Count) | Importance of reducing sheep number |
| `ADM` (Average Distance) | Fox's proximity to sheep center |
| `AMM` (Available Moves) | Preference for having move options |
| `ACM` (Capture Count) | Preference for potential captures |

> 🛑 Don’t forget to click "Accept" after tuning these variables.

---

## 📊 Statistics and Charts

Visualizations are powered by **Plotly**, including:

- ✅ **Draw Tree**: Visualizes the decision tree after each move
- ✅ **Compare**: Shows performance comparisons of algorithms (time and space complexity)

These open in your default web browser.

---

## 🧪 Benchmarking

Deepimax is benchmarked against traditional algorithms within the same environment for:
- Decision accuracy
- Resource efficiency
- Real-time game performance

---

## 📜 License

This project does not currently include a license.  
Consider adding one (e.g., MIT, Apache 2.0) to clarify reuse terms.

---

## 📬 Contact

For any questions or further collaboration, feel free to reach out via the [GitHub repository](https://github.com/alizandian/deepimax/issues).
