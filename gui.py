from customtkinter import CTk, CTkButton, CTkFrame, CTkLabel, CTkFont, CTkInputDialog, CTkTextbox, CTkEntry
from tkinter.filedialog import askopenfilename
import customtkinter as tkc
from threading import Thread
from time import sleep as wait
from simulator import Simulator
from utils import load_input_from_file


class GUI:
    __slots__ = ("app", "simulator", "width", "height", "title", "button", "sidebar", "sidebar_button_add_car",
                 "sidebar_button_run", "sidebar_button_load_from_file",
                 "sidebar_button_remove_car", "sidebar_button_clear_console", "console", "console_text", "right_frame",
                 "simulation_time_label", "simulation_time_label2", "number_of_cars_label", "number_of_cars_label2",
                 "sidebar_label", "simulation_grid_label", "simulation_grid_entry", "car_name_label", "bottom_frame",
                 "car_name_entry", "car_position_label", "car_position_entry", "car_instructions_label",
                 "car_instructions_entry", "original_input", "car_direction_label", "car_direction_entry")

    def __init__(self):
        self.app = CTk()

        self.title = "Car Simulator"
        self.width = 850
        self.height = 600

        self.simulator = Simulator()
        self.original_input = {}  # used to store the original inputs - not valid if inputs are read from file

        self.console_text = "Car Simulator using Python\n"

        self._setup_ui()

    def _setup_ui(self):
        self.app.geometry(f"{self.width}x{self.height}")
        self.app.title(self.title)

        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_columnconfigure((2, 3), weight=0)
        self.app.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar = CTkFrame(self.app, width=140, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        self.sidebar_label = CTkLabel(self.sidebar, text="Car Simulator",
                                      font=CTkFont(size=20, weight="bold"))
        self.sidebar_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_add_car = CTkButton(self.sidebar, text="Add Car", command=self._add_car)
        self.sidebar_button_add_car.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_remove_car = CTkButton(self.sidebar, text="Remove Car", command=self._remove_car)
        self.sidebar_button_remove_car.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_run = CTkButton(self.sidebar, text="Run Simulation", command=self._run_simulation)
        self.sidebar_button_run.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_clear_console = CTkButton(self.sidebar, text="Clear Console", command=self._clear_console)
        self.sidebar_button_clear_console.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="n")
        self.sidebar_button_load_from_file = CTkButton(self.sidebar, text="Load From File",
                                                       command=self._load_from_file)
        self.sidebar_button_load_from_file.grid(row=4, column=0, padx=20, pady=10, sticky="n")

        self.console = CTkTextbox(self.app, width=400)
        self.console.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsw")
        self.console.insert("0.0", self.console_text)

        self.right_frame = CTkFrame(self.app)
        self.right_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.simulation_time_label = CTkLabel(self.right_frame, text="Simulation Status", anchor="w")
        self.simulation_time_label.grid(row=0, column=0, padx=40, pady=(10, 0))
        self.simulation_time_label2 = CTkLabel(self.right_frame, text="Not Running", anchor="w", text_color="#0f0")
        self.simulation_time_label2.grid(row=1, column=0, padx=40, pady=(10, 0))
        self.number_of_cars_label = CTkLabel(self.right_frame, text="Number of Cars", anchor="w")
        self.number_of_cars_label.grid(row=2, column=0, padx=40, pady=(10, 0))
        self.number_of_cars_label2 = CTkLabel(self.right_frame, text="0", anchor="w")
        self.number_of_cars_label2.grid(row=3, column=0, padx=40, pady=(10, 0))

        self.bottom_frame = CTkFrame(self.app, width=400)
        self.bottom_frame.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.simulation_grid_label = CTkLabel(self.bottom_frame, text="Simulation grid size (width x height): ")
        self.simulation_grid_label.grid(row=1, column=1, padx=(20, 0), sticky="nsw")
        self.simulation_grid_entry = CTkEntry(self.bottom_frame, placeholder_text="100 x 100")
        self.simulation_grid_entry.grid(row=1, column=2, padx=(20, 0), pady=(10, 10), sticky="nwe")
        self.car_name_label = CTkLabel(self.bottom_frame, text="Car name: ")
        self.car_name_label.grid(row=3, column=1, padx=(20, 0), pady=(10, 10), sticky="nw")
        self.car_name_entry = CTkEntry(self.bottom_frame)
        self.car_name_entry.grid(row=3, column=2, padx=(20, 0), pady=(10, 10), sticky="nwe")
        self.car_position_label = CTkLabel(self.bottom_frame, text="Car position (x, y): ")
        self.car_position_label.grid(row=4, column=1, padx=(20, 0), pady=(10, 10), sticky="nw")
        self.car_position_entry = CTkEntry(self.bottom_frame)
        self.car_position_entry.grid(row=4, column=2, padx=(20, 0), pady=(10, 10), sticky="nwe")
        self.car_instructions_label = CTkLabel(self.bottom_frame, text="Car instructions: ")
        self.car_instructions_label.grid(row=5, column=1, padx=(20, 0), pady=(10, 10), sticky="nw")
        self.car_instructions_entry = CTkEntry(self.bottom_frame)
        self.car_instructions_entry.grid(row=5, column=2, padx=(20, 0), pady=(10, 10), sticky="nwe")
        self.car_direction_label = CTkLabel(self.bottom_frame, text="Car direction: ")
        self.car_direction_label.grid(row=6, column=1, padx=(20, 0), pady=(10, 10), sticky="nw")
        self.car_direction_entry = CTkEntry(self.bottom_frame)
        self.car_direction_entry.grid(row=6, column=2, padx=(20, 0), pady=(10, 10), sticky="nwe")

    def _load_from_file(self):
        filename = askopenfilename()
        if filename:
            for car in load_input_from_file(filename):
                self.simulator.add(*car)
        self.number_of_cars_label2.configure(text=len(self.simulator.cars))

    def _print_results(self):
        degree_direction = {0: "N", 90: "E", 180: "S", 270: "W"}
        # print simulation results
        self._print_to_console("Simulation Results\n")
        self._print_to_console("Your inputs are: ")
        for car_str in self.original_input.values():
            self._print_to_console(f"- {car_str}")
        self._print_to_console(" ")
        self._print_to_console("Completed Cars: ")
        for pos, (name, direction) in self.simulator.completed_cars.items():
            self._print_to_console(f"- Car {name} is at {pos} facing {degree_direction[direction]}")
        self._print_to_console(" ")
        if self.simulator.crashed_cars:
            self._print_to_console("Crashed Cars: ")
            for pos, cars in self.simulator.crashed_cars.items():
                for car, step in cars:
                    self._print_to_console(f"- Car {car} crashed at {pos} on step {step} with car / cars:"
                                           f" {[c for c, _ in cars if c != car]}")

        self.original_input = {}

    def status_checker(self):
        while 1:
            if self.simulator.is_running:
                self.simulation_time_label2.configure(text="Running", text_color="#f00")
            else:
                self.simulation_time_label2.configure(text="Not Running", text_color="#0f0")
                self._print_to_console("Simulation completed")
                self._print_results()
                self.number_of_cars_label2.configure(text=len(self.simulator.cars))
                break
            wait(1)

    def _run_simulation(self):
        # set the grid size
        grid_size = self.simulation_grid_entry.get()
        if grid_size:
            self.simulator.grid_x, self.simulator.grid_y = [int(val.strip()) for val in grid_size.split("x")]

        # run
        if len(self.simulator.cars):
            simulator_thread = Thread(target=self.simulator.run, args=(),
                                      daemon=True)
            simulator_thread.start()
            status_thread = Thread(target=self.status_checker, args=(),
                                   daemon=True)
            status_thread.start()
            self._print_to_console("Simulation running ...")
        else:
            self._print_to_console("No cars have been added to the simulator. Add a car before running the simulation")

    def _add_car(self):
        car_name, car_position, car_instructions, car_direction = (
            self.car_name_entry.get(), self.car_position_entry.get(),
            self.car_instructions_entry.get(), self.car_direction_entry.get())

        if not car_name or not car_position or not car_instructions or not car_direction:
            return self._print_to_console("Error: Car name, position, direction or instructions cannot be empty")

        self.original_input[car_name] = f"{car_name}, ({car_position}) {car_direction}, {car_instructions}"
        self.simulator.add(name=self.car_name_entry.get(),
                           position=tuple(int(pos.strip()) for pos in self.car_position_entry.get().split(",")),
                           direction=car_direction.upper(),
                           instructions=self.car_instructions_entry.get().upper())
        self._print_to_console(f"{self.car_name_entry.get()} added")
        self.number_of_cars_label2.configure(text=len(self.simulator.cars))

    def _remove_car(self):
        dialog = CTkInputDialog(text="Type name of the car to remove ", title="Remove car")
        car = dialog.get_input()
        if car is not None:
            car = car.strip()
        if car:
            self.simulator.remove(car)
            if car in self.original_input:
                del self.original_input[car]
            self._print_to_console(f"{car} has been removed")
        self.number_of_cars_label2.configure(text=len(self.simulator.cars))

    def _print_to_console(self, message: str):
        self.console.insert(tkc.END, f"{message}\n")

    def _clear_console(self):
        self.console.delete("1.0", tkc.END)
        self._print_to_console("Car Simulator using Python")

    def run(self):
        self.app.mainloop()
