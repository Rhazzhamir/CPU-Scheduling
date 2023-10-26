from sjf_process import *
import heapq as hp

class RR_Process(Process):
    quantom_time = None
    def __init__(self, pid, arrival_t, burst_t) -> None:
        super().__init__(pid, arrival_t, burst_t)
        self.remaining_time = self.burst_time
        self.track_service_time = []
        self.track_arrival_time = []


def round_robin_algo(memory_queue: list[RR_Process], quantom_time: int) -> list[RR_Process]:
    RR_Process.compareBy = ARRIVAL_TIME
    memory_queue.sort()
    wait_queue:   list[RR_Process] = []
    result_queue: list[RR_Process] = []
    time = 0
    while len(memory_queue) > 0 or len(wait_queue):
        if len(memory_queue) > 0 and memory_queue[-1].arrival_time <= time:
            for i in range(quantom_time):
                if memory_queue[-1].remaining_time <= 0:
                    result_queue.append(memory_queue.pop)
                    break
                memory_queue[-1].remaining_time -= 1
                time += 1
            if memory_queue[-1].remaining_time > 0:
                memory_queue[-1].track_arrival_time.append(time)
                hp.heappush(wait_queue, memory_queue.pop)
        if len(wait_queue) > 0 and wait_queue[0].remaining_time <= time:
            for i in range(quantom_time):
                if wait_queue[0].remaining_time <= 0:
                    result_queue.append(hp.heappop(wait_queue))
                    break
                wait_queue[0].remaining_time -= 1
                time += 1
            if wait_queue[0].remaining_time > 0:
                hp.heappush(wait_queue, hp.heappop(wait_queue))
