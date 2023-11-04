class RoundRobinProcess:
    quantom_time = 0

    def __init__(self, pid, arrival_t, burst_t) -> None:
        if not pid:
            raise ValueError
        self.__PID: str = pid
        self.burst_time: float | int = burst_t
        self._time_end: list[float | int] = []
        self._service_time: list[float | int] = []
        self.arrival_time: float | int = arrival_t
        self.remaining_time = self.burst_time
        self.__service_time_index = 0
        self.__time_end_index = 0

    @property
    def waiting_time(self) -> float | int:
        result = 0
        for service_time, arrival_time in zip(self._service_time, [self.arrival_time, *self._time_end]):
            result += service_time - arrival_time
        return result

    @property
    def turnaround_time(self) -> float | int:
        return self.waiting_time + self.burst_time

    @property
    def PID(self) -> str:
        return self.__PID

    @property
    def service_time(self):
        if self.__service_time_index >= len(self._service_time):
            self.__service_time_index = 0
        i = self.__service_time_index
        self.__service_time_index += 1
        return self._service_time[i]

    @property
    def time_end(self):
        if self.__time_end_index >= len(self._time_end):
            self.__time_end_index = 0
        i = self.__time_end_index
        self.__time_end_index += 1
        return self._time_end[i]

    def reset_time(self):
        self.__time_end_index = 0
        self.__service_time_index = 0

    def __repr__(self) -> str:
        return f"{self.__PID}"


def round_robin_algorithm(process_queue: list[RoundRobinProcess]):
    process_queue.sort(key=lambda x: x.arrival_time)
    gantt_chart_list: list[RoundRobinProcess] = []
    result: list[RoundRobinProcess] = []
    memory_queue: list[RoundRobinProcess] = []

    time = 0
    idle = None
    while process_queue or memory_queue:
        while process_queue and time >= process_queue[0].arrival_time:
            if idle:
                idle._time_end.append(time)
                gantt_chart_list.append(idle)
                idle = None
            memory_queue.append(process_queue.pop(0))

        if memory_queue:
            top = memory_queue.pop(0)
            top._service_time.append(time)
            remaining_quantum = min(RoundRobinProcess.quantom_time, top.remaining_time)
            gantt_chart_list.append(top)

            for _ in range(remaining_quantum):
                top.remaining_time -= 1
                time += 1
                while process_queue and time >= process_queue[0].arrival_time:
                    if idle:
                        idle._time_end.append(time)
                        gantt_chart_list.append(idle)
                        idle = None
                    memory_queue.append(process_queue.pop(0))

            if top.remaining_time > 0:
                top._time_end.append(time)
                memory_queue.append(top)
            else:
                top._time_end.append(time)
                result.append(top)
        else:
            if not idle:
                idle = RoundRobinProcess(" ", 0, 0)
                idle._service_time.append(time)
            time += 1

    return result, gantt_chart_list
