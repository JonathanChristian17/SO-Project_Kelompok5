# CPU Scheduling Algorithms Implementation

This project implements and analyzes various CPU scheduling algorithms including:
- First Come First Serve (FCFS)
- Shortest Job First (SJF)
- Round Robin (RR)
- Priority Scheduling

## Requirements

- Python 3.7+
- Required packages are listed in `requirements.txt`

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the simulation:
```bash
python simulation.py
```

This will:
1. Generate random test processes
2. Run all scheduling algorithms
3. Display the results in the console
4. Generate a comparison graph saved as 'scheduling_comparison.png'

## Project Structure

- `cpu_scheduling.py`: Contains the implementation of all scheduling algorithms
- `simulation.py`: Contains the simulation and visualization code
- `requirements.txt`: Lists all required Python packages

## Features

- Implements four major CPU scheduling algorithms
- Calculates key performance metrics:
  - Average Waiting Time
  - Average Turnaround Time
  - Average Response Time
  - Throughput
- Generates visual comparison of algorithm performance
- Supports random process generation for testing

## Analysis

The simulation provides a comprehensive comparison of different scheduling algorithms based on:
1. Waiting Time: Time a process spends waiting in the ready queue
2. Turnaround Time: Total time from submission to completion
3. Response Time: Time from submission to first execution
4. Throughput: Number of processes completed per unit time

## Notes

- Lower values for waiting time, turnaround time, and response time indicate better performance
- Higher throughput values indicate better performance
- The Round Robin algorithm uses a quantum time of 2 units by default (can be modified in simulation.py) 