from dataclasses import dataclass, field
from typing import List, Dict
from collections import deque
import copy

@dataclass
class Process:
    pid: int
    arrival_time: int
    burst_time: int
    priority: int = 0
    start_time: int = -1 # Waktu pertama kali dieksekusi
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0
    response_time: int = 0

class CPUScheduler:
    def __init__(self, processes: List[Process]):
        # Menggunakan deepcopy untuk memastikan proses asli tidak termodifikasi
        self.processes = copy.deepcopy(processes)
        self.n = len(self.processes)
        self.original_processes = copy.deepcopy(processes)

    def _reset_processes(self):
        """Mengembalikan proses ke keadaan awal sebelum tiap algoritma dijalankan."""
        self.processes = copy.deepcopy(self.original_processes)

    def _calculate_final_metrics(self) -> Dict[str, float]:
        """Menghitung metrik performa setelah semua proses selesai."""
        total_waiting_time = 0
        total_turnaround_time = 0
        total_response_time = 0
        
        last_completion_time = 0
        
        for p in self.processes:
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            p.response_time = p.start_time - p.arrival_time
            
            total_waiting_time += p.waiting_time
            total_turnaround_time += p.turnaround_time
            total_response_time += p.response_time
            
            if p.completion_time > last_completion_time:
                last_completion_time = p.completion_time
        
        return {
            'avg_waiting_time': total_waiting_time / self.n,
            'avg_turnaround_time': total_turnaround_time / self.n,
            'avg_response_time': total_response_time / self.n,
            'throughput': self.n / last_completion_time if last_completion_time > 0 else 0
        }

    def fcfs(self) -> Dict[str, float]:
        self._reset_processes()
        
        # Urutkan proses berdasarkan waktu kedatangan
        sorted_processes = sorted(self.processes, key=lambda x: x.arrival_time)
        current_time = 0
        
        for process in sorted_processes:
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            process.start_time = current_time # Pertama kali dieksekusi
            current_time += process.burst_time
            process.completion_time = current_time
        
        return self._calculate_final_metrics()

    def sjf(self) -> Dict[str, float]:
        """Shortest Job First (Non-Preemptive)"""
        self._reset_processes()
        
        remaining_processes = list(self.processes)
        current_time = 0
        completed = 0
        
        while completed < self.n:
            ready_processes = [p for p in remaining_processes if p.arrival_time <= current_time]
            
            if not ready_processes:
                current_time = min(p.arrival_time for p in remaining_processes)
                continue
            
            shortest_job = min(ready_processes, key=lambda p: p.burst_time)
            
            shortest_job.start_time = current_time
            current_time += shortest_job.burst_time
            shortest_job.completion_time = current_time
            
            remaining_processes.remove(shortest_job)
            completed += 1
            
        return self._calculate_final_metrics()

    def priority(self) -> Dict[str, float]:
        """Priority Scheduling (Non-Preemptive)"""
        self._reset_processes()
        
        remaining_processes = list(self.processes)
        current_time = 0
        completed = 0
        
        while completed < self.n:
            ready_processes = [p for p in remaining_processes if p.arrival_time <= current_time]
            
            if not ready_processes:
                current_time = min(p.arrival_time for p in remaining_processes)
                continue
            
            highest_priority_job = min(ready_processes, key=lambda p: p.priority)
            
            highest_priority_job.start_time = current_time
            current_time += highest_priority_job.burst_time
            highest_priority_job.completion_time = current_time
            
            remaining_processes.remove(highest_priority_job)
            completed += 1
            
        return self._calculate_final_metrics()

    def round_robin(self, quantum: int) -> Dict[str, float]:
        self._reset_processes()
        
        current_time = 0
        ready_queue = deque()
        processes_to_arrive = sorted(self.processes, key=lambda p: p.arrival_time)
        
        remaining_time = {p.pid: p.burst_time for p in self.processes}
        
        while processes_to_arrive or ready_queue:
            while processes_to_arrive and processes_to_arrive[0].arrival_time <= current_time:
                ready_queue.append(processes_to_arrive.pop(0))
            
            if not ready_queue:
                if processes_to_arrive:
                    current_time = processes_to_arrive[0].arrival_time
                continue

            process = ready_queue.popleft()
            
            if process.start_time == -1:
                process.start_time = current_time
            
            time_slice = min(quantum, remaining_time[process.pid])
            current_time += time_slice
            remaining_time[process.pid] -= time_slice
            
            while processes_to_arrive and processes_to_arrive[0].arrival_time <= current_time:
                ready_queue.append(processes_to_arrive.pop(0))
            
            if remaining_time[process.pid] > 0:
                ready_queue.append(process)
            else:
                process.completion_time = current_time
                
        return self._calculate_final_metrics()