import customtkinter as ctk
from sjf_process import *
from CTkMessagebox import CTkMessagebox


FRAME_STYLE = {"border color": "white", "border width": 1}
root = ctk.CTk()
root.title("CPU Scheduling Algorithms")
root.resizable = True
root.geometry("1000x520")
mainframe = ctk.CTkFrame(root)

mainframe.pack(expand=True, fill="both")
mainframe.grid_columnconfigure(0, weight=1)
mainframe.grid_columnconfigure(1, weight=1)
mainframe.grid_rowconfigure(1, weight=1)


header_frame = ctk.CTkFrame(
    mainframe,
    height=80,
    border_color=FRAME_STYLE["border color"],
    border_width=FRAME_STYLE["border width"],
)
input_frame = ctk.CTkScrollableFrame(
    mainframe,
    height=500,
    border_color=FRAME_STYLE["border color"],
    border_width=FRAME_STYLE["border width"],
)
result_frame = ctk.CTkFrame(
    mainframe,
    border_color=FRAME_STYLE["border color"],
    border_width=FRAME_STYLE["border width"]
)

header_frame.grid(row=0, column=0, columnspan=2, sticky=ctk.NSEW)
input_frame.grid(row=1, column=0, sticky=ctk.NSEW)
result_frame.grid(row=1, column=1, sticky=ctk.NSEW)


# ---------------------------------------------------- #
# ---------------------- HEADER ---------------------- #
# ---------------------------------------------------- #

choice = ["SJF Algorithm", "Round Robin Algorithm"]
process_var = ctk.StringVar(value=choice[0])
num_of_process_var = ctk.IntVar(value=3)

slider_label = ctk.CTkLabel(header_frame, text="Number of process: ")
slider_output = ctk.CTkLabel(header_frame, text=f"{num_of_process_var.get():02}")


def select_algo(choice):
    process_var.set(choice)
    create_table(None)


def select_number_of_process(value):
    num_of_process_var.set(value)
    slider_output.configure(text=f"{num_of_process_var.get():02}")


process_select = ctk.CTkComboBox(
    header_frame,
    values=choice,
    command=select_algo,
    variable=process_var
)

num_of_process_slider = ctk.CTkSlider(
    header_frame, from_=1, to=30,
    command=select_number_of_process
)
num_of_process_slider.set(num_of_process_var.get())
start_process_button = ctk.CTkButton(header_frame, text="Start Process", border_color="white")

process_select.grid(row=0, column=0, pady=10, padx=10)
slider_label.grid(row=0, column=1, pady=10, padx=10)
num_of_process_slider.grid(row=0, column=3, pady=10, padx=10)
slider_output.grid(row=0, column=2, pady=10, padx=10)
start_process_button.grid(row=0, column=10, pady=10, padx=10)



# ---------------------------------------------------- #
# ---------------------- BODY ------------------------ #
# ---------------------------------------------------- #
values: tuple[int, ctk.IntVar, ctk.IntVar] = None
process_queue: list[Process] = []
table_container: tuple[ctk.CTkFrame, tuple] = None
chart_container = ctk.CTkScrollableFrame(result_frame, fg_color='transparent', orientation='horizontal', border_width=2, border_color='white')
chart_container.pack(anchor=ctk.NW, expand=True, fill='both', ipadx=5, ipady=5)
calculated_result = ctk.CTkScrollableFrame(result_frame, fg_color='transparent', border_width=2, border_color='white')
calculated_result.pack(anchor=ctk.NW, expand=True, fill='both', ipadx=5, ipady=5)

def destroy_children(parent: ctk.CTkFrame | ctk.CTkScrollableFrame):
    for child in parent.winfo_children():
        child.destroy()

def create_table(event):
    global table_container
    global values
    global process_queue

    if table_container != None:
        table_container.destroy()

    table_container, values = None, None
    process_queue = []

    match process_var.get():
        case "SJF Algorithm":
            TEMP = sjf_input_table(input_frame, num_of_process_var.get())
            table_container = TEMP["table"]
            values = TEMP["values"]
        case "Round Robin Algorithm":
            ...

def generate_result():
    global calculated_result
    global process_queue
    destroy_children(calculated_result)

    table_label = ctk.CTkLabel(calculated_result, text='RESULT TABLE:', font=ctk.CTkFont(size=18, weight='bold'))
    table_label.pack(anchor=ctk.NW, pady=(3, 20))

    table_frame = ctk.CTkFrame(calculated_result)
    table_frame.pack(anchor=ctk.NW)

    tbl_header = ("Process ID", "Waiting Time", "Turn around Time")

    for i, header in enumerate(tbl_header):
        frame = ctk.CTkFrame(table_frame, border_color="white", border_width=1, corner_radius=0)
        frame.grid(column=i, row=0, sticky="nsew")
        text = ctk.CTkLabel(frame, text=header)
        text.pack(pady=2, padx=20)
        table_frame.columnconfigure(i, weight=1)
    
    for key, val in enumerate(process_queue):
            for i, p in enumerate([val.PID, val.waiting_time, val.turnaround_time]):
                frame = ctk.CTkFrame(table_frame, border_color="white", border_width=1, corner_radius=0)
                frame.grid(column=i, row=key + 1, sticky="nsew")
                text = ctk.CTkLabel(frame, text=p)
                text.pack(pady=2, padx=40)
                table_frame.columnconfigure(i, weight=1)
    start_process_button.configure

    wt_calc_ave = sum([p.waiting_time for p in process_queue]) / len(process_queue)
    tt_calc_ave = sum([p.turnaround_time for p in process_queue]) / len(process_queue)
    waiting_time_ave = ctk.CTkLabel(calculated_result, text=f"Average Waiting Time: {wt_calc_ave:.2f}ms", font=ctk.CTkFont(size=14, weight='bold'))
    waiting_time_ave.pack(anchor=ctk.NW, pady=(3, 0))
    turnarount_time_ave = ctk.CTkLabel(calculated_result, text=f"Average Turn around Time: {tt_calc_ave:.2f}ms", font=ctk.CTkFont(size=14, weight='bold'))
    turnarount_time_ave.pack(anchor=ctk.NW, pady=0)


def generate_GANTT_chart():
    global process_queue
    global chart_container
    destroy_children(chart_container)

    chart_label = ctk.CTkLabel(chart_container, text='GANTT CHART:', font=ctk.CTkFont(size=18, weight='bold'))
    colspan = len(process_queue) + 2
    chart_label.grid(row=0, column=0, columnspan=colspan, pady=20, sticky=ctk.W)

    col = 0
    WIDTH = 10
    if process_queue[0].service_time != 0:
            column_width = WIDTH * process_queue[0].service_time
            column_width = int(column_width)

            frame = ctk.CTkFrame(chart_container, border_color='white', border_width=1, corner_radius=0)
            frame.grid(row=1, column=col, ipadx=column_width)
            time = ctk.CTkLabel(chart_container, text='0', fg_color='transparent')
            time.grid(row=2, column=col, padx=(0, column_width), ipadx=0, sticky=ctk.W)
            col += 1

            text = ctk.CTkLabel(frame, text='')
            text.pack(pady=2, padx=WIDTH)
    
    for p in process_queue:
        column_width = WIDTH *(p.time_end - p.service_time)
        column_width = int(column_width)

        frame = ctk.CTkFrame(chart_container, border_color='white', border_width=1, corner_radius=0)
        frame.grid(row=1, column=col, ipadx=column_width)
        time = ctk.CTkLabel(chart_container, text=p.service_time, fg_color='transparent')
        time.grid(row=2, column=col, padx=(0, column_width), ipadx=0, sticky=ctk.W)
        col += 1

        text = ctk.CTkLabel(frame, text=p.PID)
        text.pack(pady=2)
    
    time = ctk.CTkLabel(chart_container, text=process_queue[-1].time_end, fg_color='transparent')
    time.grid(row=2, column=col, padx=(0, column_width), ipadx=0, sticky=ctk.W)


def process_start():
    global process_queue

    for i in range(len(values)):
        try:
            pid: str = values[i][PID]
            at = int(values[i][ARRIVAL_TIME].get())
            bt = int(values[i][BURST_TIME].get())
            process_queue.append(Process(pid, at, bt))
        except ValueError:
            CTkMessagebox(title="Info", message="Please fill the entry!")
            return

    process_queue = sjf_algorithm(process_queue)
    generate_GANTT_chart()
    Process.compareBy = PID
    process_queue.sort()
    generate_result()


num_of_process_slider.bind("<ButtonRelease-1>", create_table)
start_process_button.configure(command=process_start)
create_table(None)

root.mainloop()
