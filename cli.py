from simulator import Simulator

"""
    This is the CLI version of the car simulator. Use this as a fallback if GUI cannot be used due to some restriction
"""


class CLI:
    def __init__(self):
        self.simulator = Simulator()
        self.original_input = {}

        self.screen_1 = """
Welcome to Auto Driving Car Simulation!

Please enter the width and height of the simulation field in x y format: """

        self.screen_2 = """
Please choose from the following options:

[1] Add a car to field
[2] Run simulation
        
"""

        self.screen_3 = """
Please choose from the following options:

[1] Start over
[2] Exit
        
"""

    def run(self):
        grid_size = input(self.screen_1)
        self.simulator.grid_x, self.simulator.grid_y = [int(val.strip()) for val in grid_size.split(" ")]
        print(f"You have created a field of {self.simulator.grid_x} x {self.simulator.grid_y}")
        self.show_main_menu()

    def show_main_menu(self):
        response = int(input(self.screen_2))
        if response == 1:
            self.show_add_car_menu()
        elif response == 2:
            self.run_simulation()
        else:
            print("Invalid option")
            self.show_main_menu()

    def show_add_car_menu(self):
        car_name = input("Please enter the name of the car: ")
        response_segments = (input(f"Please enter initial position of car {car_name} in x y Direction format: ")
                             .split(" "))
        pos = int(response_segments[0].strip()), int(response_segments[1].strip())
        direction = response_segments[2].strip().upper()
        instructions = input(f"Please enter the commands for car {car_name}: ").upper()

        self.original_input[car_name] = f"{car_name}, {pos} {direction}, {instructions}"
        self.simulator.add(car_name, pos, direction, instructions)

        print("Your current list of cars are: ")
        for car in self.original_input.values():
            print(f"- {car}")
        self.show_main_menu()

    def run_simulation(self):
        self.simulator.run()
        self.print_results()

    def print_results(self):
        degree_direction = {0: "N", 90: "E", 180: "S", 270: "W"}
        # print simulation results
        print("Simulation Results\n")
        print("Your current list of cars is: ")
        for car_str in self.original_input.values():
            print(f"- {car_str}")
        print(" ")
        print("After simulation the result is: ")
        print("Completed Cars: ")
        for pos, (name, direction) in self.simulator.completed_cars.items():
            print(f"- {name}, {pos} {degree_direction[direction]}")
        print(" ")
        if self.simulator.crashed_cars:
            print("Crashed Cars: ")
            for pos, cars in self.simulator.crashed_cars.items():
                for car, step in cars:
                    print(f"- {car} crashed at {pos} on step {step} with car / cars:"
                          f" {[c for c, _ in cars if c != car]}")

        self.show_final_screen()

    def show_final_screen(self):
        response = int(input(self.screen_3))
        if response == 1:
            self.run()
        elif response == 2:
            print("Thank you for running the simulation. Goodbye!")
        else:
            print("Invalid option")
            self.show_final_screen()


def main():
    CLI().run()


if __name__ == "__main__":
    main()
