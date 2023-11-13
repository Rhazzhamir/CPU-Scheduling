import heapq as hp
import customtkinter as ctk

PID = 0
ARRIVAL_TIME = 1
BURST_TIME = 2


class NonPreempProcess:
    compareBy = PID

    def __init__(self, pid, arrival_t, burst_t) -> None:
        if not pid:
            raise ValueError
        self.__PID:                   str = pid
        self.arrival_time:    float | int = arrival_t
        self.burst_time:      float | int = burst_t
        self.service_time:    float | int = None
        self.time_end:        float | int = None
        self.remaining_time:  float | int = burst_t

    @property
    def waiting_time(self) -> float | int:
        return self.service_time - self.arrival_time

    @property
    def turnaround_time(self) -> float | int:
        return self.waiting_time + self.burst_time

    @property
    def PID(self) -> str:
        return self.__PID

    def __lt__(self, __value: object) -> bool:
        if NonPreempProcess.compareBy == PID:
            return self.PID < __value.PID
        elif NonPreempProcess.compareBy == ARRIVAL_TIME:
            return self.arrival_time < __value.arrival_time
        elif NonPreempProcess.compareBy == BURST_TIME:
            if self.burst_time == __value.burst_time:
                return self.arrival_time < __value.arrival_time
            return self.burst_time < __value.burst_time

    def __gt__(self, __value: object) -> bool:
        if NonPreempProcess.compareBy == PID:
            return self.PID > __value.PID
        elif NonPreempProcess.compareBy == ARRIVAL_TIME:
            return self.arrival_time > __value.arrival_time
        elif NonPreempProcess.compareBy == BURST_TIME:
            if self.burst_time == __value.burst_time:
                return self.arrival_time > __value.arrival_time
            return self.burst_time > __value.burst_time

    def __repr__(self) -> str:
        return f"{self.__PID}"


def sjf_algorithm(process_queue: list[NonPreempProcess]) -> list[NonPreempProcess]:
    process_queue.reverse()
    process_queue.sort(reverse=True, key=lambda x: x.arrival_time)
    NonPreempProcess.compareBy = BURST_TIME
    result: list[NonPreempProcess] = []
    gantt_chart_list: list[NonPreempProcess] = []
    memory_queue: list[NonPreempProcess] = []
    time = 0
    idle = None

    while process_queue or memory_queue:
        while process_queue and time >= process_queue[-1].arrival_time:
            if idle:
                idle.time_end = time
                gantt_chart_list.append(idle)
                idle = None
            hp.heappush(memory_queue, process_queue.pop())

        if memory_queue:
            top = hp.heappop(memory_queue)
            top.service_time = time
            gantt_chart_list.append(top)

            while top.remaining_time:
                time += 1
                top.remaining_time -= 1
                while process_queue and time >= process_queue[-1].arrival_time:
                    hp.heappush(memory_queue, process_queue.pop())
            top.time_end = time
            result.append(top)
        else:
            if not idle:
                idle = NonPreempProcess(" ", 0, 0)
                idle.service_time = time
            time += 1

    return result, gantt_chart_list
