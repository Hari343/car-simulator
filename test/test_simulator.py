from simulator import Simulator
from unittest import TestCase


class TestSimulator(TestCase):
    __slots__ = "simulator"

    def setUp(self):
        self.simulator = Simulator()

    def test_default_state(self):
        assert self.simulator.grid_x == self.simulator.grid_y == 100
        assert not self.simulator.cars and not self.simulator.completed_cars and not self.simulator.crashed_cars

    def test_run_with_no_cars(self):
        self.simulator.run()
        assert not self.simulator.completed_cars and not self.simulator.crashed_cars

    def test_add_car(self):
        car = "Car", (5, 4), "E", "LRLRLRLRLRLR"
        self.simulator.add(*car)
        assert len(self.simulator.cars) == 1
        assert self.simulator.cars["Car"] == [(5, 4), 90, bytearray(car[3], encoding="utf-8")]

    def test_run_with_one_car(self):
        car = "Car", (5, 4), "E", "LRLRLRLRLRLR"
        self.simulator.add(*car)
        self.simulator.run()
        assert not self.simulator.cars
        assert len(self.simulator.completed_cars) == 1
        assert self.simulator.completed_cars[(5, 4)] == ("Car", 90)

    def test_scenario_1(self):
        # Scenario 1:
        # grid: 1000 x 1000
        # car: Pagani Zonda init_pos: 500, 0 direction: N Going in a straight line
        # results: should reach 500, 999. No crashes
        self.simulator.grid_x = self.simulator.grid_y = 1_000
        self.simulator.add("Pagani Zonda", (500, 0), "N", "F" * 999)
        self.simulator.run()
        assert not self.simulator.crashed_cars
        assert self.simulator.completed_cars[(500, 999)] == ("Pagani Zonda", 0)

        # same scenario as above but overshoots map boundaries, also verifies Simulator instance's reusability
        self.simulator.add("Pagani Zonda", (500, 0), "N", "F" * 9999)
        assert len(self.simulator.cars) == 1
        self.simulator.run()
        assert not self.simulator.crashed_cars
        assert len(self.simulator.completed_cars) == 1
        assert self.simulator.completed_cars[(500, 999)] == ("Pagani Zonda", 0)

    def test_scenario_2(self):
        # Scenario 2:
        # grid: 1000 x 1000
        # car: Koensigg CCXR init_pos: 0, 0 direction: N Going around the map
        # results: should end at where it started 0, 0 No crashes
        self.simulator.grid_x = self.simulator.grid_y = 1_000
        self.simulator.add("Koensigg CCXR", (0, 0), "N",
                      "F" * 999 + "R" + "F" * 999 + "R" + "F" * 999 + "R" + "F" * 999 + "R")
        self.simulator.run()
        assert not self.simulator.crashed_cars
        assert self.simulator.completed_cars[(0, 0)] == ("Koensigg CCXR", 0)

    def test_scenario_3(self):
        # Scenario 3:
        # grid: 1000 x 1000
        # car: Koensigg CCXR init_pos: 0, 0 direction: N Going around the map
        # car: Pagani Zonda init_pos: 999, 0 direction: W Going around the map
        # results: both should end at where it started. No crashes
        self.simulator.grid_x = self.simulator.grid_y = 1_000
        self.simulator.add("Koensigg CCXR", (0, 0), "N",
                      "F" * 999 + "R" + "F" * 999 + "R" + "F" * 999 + "R" + "F" * 999 + "R")
        self.simulator.add("Pagani Zonda", (999, 0), "W",
                      "F" * 999 + "R" + "F" * 999 + "R" + "F" * 999 + "R" + "F" * 999 + "R")
        self.simulator.run()
        assert not self.simulator.crashed_cars
        assert self.simulator.completed_cars[(0, 0)] == ("Koensigg CCXR", 0)
        assert self.simulator.completed_cars[(999, 0)] == ("Pagani Zonda", 270)

    def test_scenario_4(self):
        # Scenario 4:
        # grid: 1000 x 1000
        # car: Lamborghini Superveloce init_pos 0, 0 direction: "E" Full map traversal
        # Results: end at 0, 999 No crashes
        self.simulator.grid_x = self.simulator.grid_y = 1_000
        instructions = []
        for i in range(1_000):
            if not i % 2:
                instructions.append("F" * 999 + "LFL")
            else:
                instructions.append("F" * 999 + "RFR")
        self.simulator.add("Lamborghini Superveloce", (0, 0), "E", "".join(instructions))
        self.simulator.run()
        assert not self.simulator.crashed_cars
        assert self.simulator.completed_cars[(0, 999)] == ("Lamborghini Superveloce", 90)

    def test_scenario_5(self):
        # Scenario 5:
        # grid: 1000 x 1000
        # car: Koensigg CCXR init_pos: 0, 0 direction: N Going straight and turning right
        # car: Pagani Zonda init_pos: 999, 999 direction: S Going straight and turning right
        # results: both should NOT crash
        self.simulator.grid_x = self.simulator.grid_y = 1_000
        self.simulator.add("Koensigg CCXR", (0, 0), "N",
                      "F" * 499 + "R" + "F" * 999)
        self.simulator.add("Pagani Zonda", (999, 999), "S",
                      "F" * 499 + "R" + "F" * 999)
        self.simulator.run()
        assert not self.simulator.crashed_cars
        assert self.simulator.completed_cars[(999, 499)] == ("Koensigg CCXR", 90)
        assert self.simulator.completed_cars[(0, 500)] == ("Pagani Zonda", 270)

    def test_scenario_6(self):
        # Scenario 6:
        # grid: 1000 x 1000
        # car: Koensigg CCXR init_pos: 0, 0 direction: N Going straight and turning right
        # car: Pagani Zonda init_pos: 999, 999 direction: S Going straight and turning right
        # results: both should crash
        self.simulator.grid_x = self.simulator.grid_y = 1_000
        self.simulator.add("Koensigg CCXR", (0, 0), "N",
                      "F" * 499 + "R" + "F" * 999)
        self.simulator.add("Pagani Zonda", (999, 999), "S",
                      "F" * 500 + "R" + "F" * 999)
        self.simulator.run()
        assert not self.simulator.completed_cars
        assert self.simulator.crashed_cars[(500, 499)] == [("Koensigg CCXR", 1_000), ("Pagani Zonda", 1_000)]
