import customtkinter as ctk
from round_robin_process import *

def validate_integer_input(P: str):
    return P == "" or P.isdigit()


def input_table(input_frame: ctk.CTkFrame | ctk.CTkScrollableFrame, num_of_process: int, process_type="") -> tuple[ctk.CTkFrame, tuple]:
    values: tuple[int, ctk.StringVar, ctk.StringVar] = [None] * num_of_process

    table_container = ctk.CTkFrame(input_frame)
    table_container.pack(anchor=ctk.W, pady=10, padx=10)

    PID_frame = ctk.CTkFrame(table_container, border_color="white", border_width=1, corner_radius=0)
    PID_frame.grid(row=0, column=0, sticky="nsew")
    PID_label = ctk.CTkLabel(PID_frame, text="Process ID")
    PID_label.pack(padx=41, pady=2)

    arrival_frame = ctk.CTkFrame(table_container, border_color="white", border_width=1, corner_radius=0)
    arrival_frame.grid(row=0, column=1, sticky="nsew")
    arrival_t_label = ctk.CTkLabel(arrival_frame, text="Arrival Time")
    arrival_t_label.pack(padx=37, pady=2)

    burst_frame = ctk.CTkFrame(table_container, border_color="white", border_width=1, corner_radius=0)
    burst_frame.grid(row=0, column=2, sticky="nsew")
    burst_t_label = ctk.CTkLabel(burst_frame, text="Burst Time")
    burst_t_label.pack(padx=38, pady=2)
    table_container.columnconfigure(0, weight=1)
    table_container.columnconfigure(1, weight=1)
    table_container.columnconfigure(2, weight=1)
    

    for i in range(1, num_of_process + 1):
        burst_time_var = ctk.StringVar(value='')
        arrival_time_var = ctk.StringVar(value='')
        
        frame = ctk.CTkFrame(table_container, border_color="white", border_width=1, corner_radius=0)
        frame.grid(row=i, column=0, sticky="nsew")
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
        arrival_t_input.grid(row=i, column=1, ipady=2, sticky="nsew")

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
        burst_t_input.grid(row=i, column=2, ipady=2, sticky="nsew")
        values[i-1] = (f"P{i:02}", arrival_time_var, burst_time_var)
        table_container.columnconfigure(0, weight=1)
        table_container.columnconfigure(1, weight=1)
        table_container.columnconfigure(2, weight=1)
    
    return table_container, values

def round_robin_input(input_frame: ctk.CTkFrame | ctk.CTkScrollableFrame, num_of_process: int, process_type="") -> tuple[ctk.CTkFrame, tuple]:
    quantum_time_var = ctk.StringVar(value='')
    table_container, values = input_table(input_frame, num_of_process)
    quantum_time_label = ctk.CTkLabel(
        table_container,
        text="Quantum Time: ",
        fg_color="transparent"
    )
    quantum_time_entry = ctk.CTkEntry(
        table_container,
        fg_color="transparent",
        corner_radius=0,
        border_width=1,
        textvariable=quantum_time_var
    )
    quantum_time_entry.configure(
        validate='all',
        validatecommand=(table_container.register(
            validate_integer_input), "%P"),
        justify="left"
    )
    quantum_time_label.grid(
        row=num_of_process + 1,
        column=0,
        ipady=2,
        sticky="nsew"
    )
    quantum_time_entry.grid(
        row=num_of_process + 1,
        column=1,
        ipady=2,
        sticky="nsew",
        columnspan=2
    )
    return table_container, values, quantum_time_var
