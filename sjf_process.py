import heapq as hp
import customtkinter as ctk

PID = 0
ARRIVAL_TIME = 1
BURST_TIME = 2

class Process:
    compareBy = PID
    def __init__(self, pid, arrival_t, burst_t) -> None:
        if not pid:
            raise ValueError
        self.__PID:                   str = pid
        self.arrival_time:    float | int = arrival_t
        self.burst_time:      float | int = burst_t
        self.service_time:    float | int = None
        self.time_end:        float | int = None
    
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
        if Process.compareBy == PID:
            return self.PID < __value.PID
        elif Process.compareBy == ARRIVAL_TIME:
            return self.arrival_time < __value.arrival_time
        elif Process.compareBy == BURST_TIME:
            return self.burst_time < __value.burst_time

    def __gt__(self, __value: object) -> bool:
        if Process.compareBy == PID:
            return self.PID > __value.PID
        elif Process.compareBy == ARRIVAL_TIME:
            return self.arrival_time > __value.arrival_time
        elif Process.compareBy == BURST_TIME:
            return self.burst_time > __value.burst_time

def sjf_algorithm(memory_queue: list[Process]) -> list[Process]:
    Process.compareBy = ARRIVAL_TIME
    memory_queue.sort(reverse=True)
    Process.compareBy = BURST_TIME
    result:         list[Process] = []
    wait_queue:     list[Process] = []
    current_process:    Process = None
    time = 0
    
    while (len(memory_queue) > 0 or len(wait_queue) > 0):
        if len(memory_queue) > 0 and memory_queue[-1].arrival_time <= time:
            if current_process and current_process.time_end > time:
                hp.heappush(wait_queue, memory_queue.pop())
            else:
                current_process = memory_queue.pop()
                current_process.service_time = time
                current_process.time_end = time + current_process.burst_time
                result.append(current_process)
        elif len(wait_queue) > 0 and (current_process and current_process.time_end <= time):
            current_process = hp.heappop(wait_queue)
            current_process.service_time = time
            current_process.time_end = time + current_process.burst_time
            result.append(current_process)
        else:
            time += 1
            
    return result


def validate_integer_input(P: str):
    return P == "" or P.isdigit()


def sjf_input_table(input_frame: ctk.CTkFrame | ctk.CTkScrollableFrame, num_of_process: int) -> dict[ctk.CTkFrame, tuple]:
    values: tuple[int, ctk.StringVar, ctk.StringVar] = [None] * num_of_process

    table_container = ctk.CTkFrame(input_frame)
    table_container.pack(anchor=ctk.W, pady=10, padx=10)

    PID_frame = ctk.CTkFrame(table_container, border_color="white", border_width=1, corner_radius=0)
    PID_frame.grid(row=0, column=0)
    PID_label = ctk.CTkLabel(PID_frame, text="Process ID")
    PID_label.pack(padx=41, pady=2)

    arrival_frame = ctk.CTkFrame(table_container, border_color="white", border_width=1, corner_radius=0)
    arrival_frame.grid(row=0, column=1)
    arrival_t_label = ctk.CTkLabel(arrival_frame, text="Arrival Time")
    arrival_t_label.pack(padx=37, pady=2)

    burst_frame = ctk.CTkFrame(table_container, border_color="white", border_width=1, corner_radius=0)
    burst_frame.grid(row=0, column=2)
    burst_t_label = ctk.CTkLabel(burst_frame, text="Burst Time")
    burst_t_label.pack(padx=38, pady=2)
    

    for i in range(1, num_of_process + 1):
        burst_time_var = ctk.StringVar(value='')
        arrival_time_var = ctk.StringVar(value='')
        
        frame = ctk.CTkFrame(table_container, border_color="white", border_width=1, corner_radius=0)
        frame.grid(row=i, column=0)
        pid_label = ctk.CTkLabel(frame, text=f"P{i:02}")
        pid_label.pack(padx=60, pady=2)

        arrival_t_input = ctk.CTkEntry(
            table_container, 
            border_color="white", 
            border_width=1, 
            corner_radius=0,
            textvariable=arrival_time_var
        )
        arrival_t_input.configure(
            validate='all', 
            validatecommand=(table_container.register(validate_integer_input), '%P'),
            justify="center"
        )
        arrival_t_input.grid(row=i, column=1, ipady=2)

        burst_t_input = ctk.CTkEntry(
            table_container, 
            border_color="white", 
            border_width=1, 
            corner_radius=0,
            textvariable=burst_time_var
        )
        burst_t_input.configure(
            validate='all', 
            validatecommand=(table_container.register(validate_integer_input), '%P'),
            justify="center"
        )
        burst_t_input.grid(row=i, column=2, ipady=2)
        values[i-1] = (f"P{i:02}", arrival_time_var, burst_time_var)
    
    return {"table": table_container, "values": values}