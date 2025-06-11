from cpu_scheduling import Process, CPUScheduler 
import matplotlib.pyplot as plt
import numpy as np

def generate_test_processes(n_processes: int = 5) -> list[Process]:
    """Generate random test processes"""
    processes = []
    np.random.seed(42) 
    for i in range(n_processes):
        processes.append(Process(
            pid=i+1,
            arrival_time=np.random.randint(0, 10),
            burst_time=np.random.randint(1, 20),
            priority=np.random.randint(1, 10)
        ))
    return processes


def run_simulation(n_processes: int = 5, quantum: int = 4): 
    """Run simulation with all algorithms"""
    processes = generate_test_processes(n_processes)
    scheduler = CPUScheduler(processes)
    
    results = {
        'FCFS': scheduler.fcfs(),
        'SJF': scheduler.sjf(),
        'Round Robin': scheduler.round_robin(quantum),
        'Priority': scheduler.priority()
    }
    
    return results, processes 

def plot_results(results: dict):
    """Plot comparison of different algorithms"""
    metrics = ['avg_waiting_time', 'avg_turnaround_time', 'avg_response_time', 'throughput']
    algorithms = list(results.keys())
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('CPU Scheduling Algorithms Comparison')
    
    for idx, metric in enumerate(metrics):
        row = idx // 2
        col = idx % 2
        ax = axes[row, col]
        values = [results[algo][metric] for algo in algorithms]
        
        bars = ax.bar(algorithms, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        ax.set_title(metric.replace('_', ' ').title())
        ax.set_ylabel('Time (units)' if 'time' in metric else 'Processes/Unit Time')
        
        ax.bar_label(bars, fmt='%.2f')
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('scheduling_comparison.png')
    plt.close()

def print_process_details(processes: list[Process]):
    """Print details of test processes"""
    print("Test Processes:")
    # Header tabel
    print(f"{'PID':<5} {'Arrival Time':<15} {'Burst Time':<15} {'Priority':<10}")
    print("-" * 50)
    # Data proses
    for p in processes:
        print(f"{p.pid:<5} {p.arrival_time:<15} {p.burst_time:<15} {p.priority:<10}")

def main():
    # Run simulation
    results, processes = run_simulation(n_processes=5, quantum=4)
    
    # Print process details
    print_process_details(processes)
    
    # Print results
    print("\n" + "="*20 + " RESULTS " + "="*20)
    for algo, metrics in results.items():
        print(f"\nAlgorithm: {algo}")
        print("-" * 30)
        for metric, value in metrics.items():
            print(f"{metric.replace('_', ' ').title():<22}: {value:.2f}")
    print("="*49)
    
    # Plot results
    plot_results(results)
    print("\nChart of results has been saved as 'scheduling_comparison.png'")

if __name__ == "__main__":
    main()