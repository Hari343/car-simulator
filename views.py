from abc import ABC, abstractmethod
from typing import Any
from exceptions import InvalidInputError

"""
    This module contains several Views, Each View should implement
    a _render method which should return parsed user input back to the calling subroutine, if the view requires user
     input
"""


class View(ABC):

    @abstractmethod
    def _render(self, *args, **kwargs) -> Any:
        pass

    def render(self, *args, **kwargs) -> Any:
        while 1:
            try:
                return self._render(*args, **kwargs)
            except InvalidInputError as e:
                print(e.args[0])
                continue


class StartMenuView(View):
    def __init__(self):
        super()
        self.content = """
Welcome to Auto Driving Car Simulation!

Please enter the width and height of the simulation field in x y format: """

    def _render(self) -> tuple[int, int]:
        response = input(self.content).strip()
        segments = response.split(" ")
        error_msg = "The input should be in 'x y' format"

        if len(segments) != 2:
            raise InvalidInputError(error_msg)

        try:
            x, y = int(segments[0].strip()), int(segments[1].strip())
        except ValueError:
            raise InvalidInputError(error_msg)

        return x, y


class MainMenuView(View):
    def __init__(self):
        super()
        self.content = """
Please choose from the following options:

[1] Add a car to field
[2] Run simulation
        
"""

    def _render(self) -> int:
        response = input(self.content).strip()
        if response not in {"1", "2"}:
            raise InvalidInputError("Enter just 1 or 2")
        return int(response)


class AddCarView(View):
    def __init__(self):
        super()

    def _render(self) -> tuple[str, tuple, str, str]:
        car_name = input("Please enter the name of the car: ")

        response = input("Please enter the initial pos of the car in x y direction format: ").strip()
        response_segments = response.split(" ")
        if len(response_segments) != 3:
            raise InvalidInputError("Input should be in 'x y direction' format")

        try:
            x, y = int(response_segments[0].strip()), int(response_segments[1].strip())
        except ValueError:
            raise InvalidInputError("x, y both should be integers")

        direction = response_segments[2].upper()
        if direction not in "NSEW":
            raise InvalidInputError("direction should be either 'N', 'S', 'W' or 'E'")

        commands = input("Please enter the commands for the car: ").strip().upper()

        if not all(c not in "FRL" for c in response):
            raise InvalidInputError("Only commands 'F', 'R', 'L' are supported")

        return car_name, (x, y), direction, commands


class ListCarView(View):
    def __init__(self):
        super()

    def _render(self, cars: list) -> None:
        degree_direction = {0: "N", 90: "E", 180: "S", 270: "W"}
        print("Your current list of cars are: ")
        for car in cars:
            *pos, direction = car.initial_pos
            print(f"- {car.name}, {tuple(pos)} {degree_direction[direction]}, {car.instructions}")


class ResultsView(View):
    def __init__(self):
        super()

    def _render(self, completed_cars, crashed_cars) -> None:
        degree_direction = {0: "N", 90: "E", 180: "S", 270: "W"}
        # print simulation results
        print("Simulation Results")
        print(" ")
        print("Completed Cars: ")
        for pos, (name, direction) in completed_cars.items():
            print(f"- {name}, {pos} {degree_direction[direction]}")
        print(" ")
        if crashed_cars:
            print("Crashed Cars: ")
            for pos, cars in crashed_cars.items():
                for car, step in cars:
                    print(f"- {car} crashed at {pos} on step {step} with car / cars:"
                          f" {[c for c, _ in cars if c != car]}")


class StartOverView(View):
    def __init__(self):
        super()
        self.content = """
Please choose from the following options:

[1] Start Over
[2] Exit

"""

    def _render(self) -> int:
        response = input(self.content).strip()
        if response not in {"1", "2"}:
            raise InvalidInputError("Enter just 1 or 2")
        return int(response)


class GoodbyeView(View):
    def __init__(self):
        super()
        self.content = "Thank you for running the simulation. Goodbye!"

    def _render(self) -> None:
        print(self.content)
