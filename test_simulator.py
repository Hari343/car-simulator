from simulator import Simulator


def main():
    simulator = Simulator()

    # Scenario 1:
    # grid: 1000 x 1000
    # car: Pagani Zonda init_pos: 500, 0 direction: N Going in a straight line
    # results: should reach 500, 999. No crashes
    simulator.grid_x = simulator.grid_y = 1_000
    simulator.add("Pagani Zonda", (500, 0), "N", "F" * 999)
    simulator.run()
    assert not simulator.crashed_cars
    assert simulator.completed_cars[(500, 999)] == ("Pagani Zonda", 0)

    # same scenario but overshoots map boundaries
    simulator.add("Pagani Zonda", (500, 0), "N", "F" * 9999)
    simulator.run()
    assert not simulator.crashed_cars
    assert simulator.completed_cars[(500, 999)] == ("Pagani Zonda", 0)

    # Scenario 2:
    # grid: 1000 x 1000
    # car: Koensigg CCXR init_pos: 0, 0 direction: N Going around the map
    # results: should end at where it started 0, 0 No crashes
    simulator.add("Koensigg CCXR", (0, 0), "N",
                  "F" * 999 + "R" + "F" * 999 + "R" + "F" * 999 + "R" + "F" * 999 + "R")
    simulator.run()
    assert not simulator.crashed_cars
    assert simulator.completed_cars[(0, 0)] == ("Koensigg CCXR", 0)

    # Scenario 3:
    # grid: 1000 x 1000
    # car: Koensigg CCXR init_pos: 0, 0 direction: N Going around the map
    # car: Pagani Zonda init_pos: 999, 0 direction: W Going around the map
    # results: both should end at where it started. No crashes
    simulator.add("Koensigg CCXR", (0, 0), "N",
                  "F" * 999 + "R" + "F" * 999 + "R" + "F" * 999 + "R" + "F" * 999 + "R")
    simulator.add("Pagani Zonda", (999, 0), "W",
                  "F" * 999 + "R" + "F" * 999 + "R" + "F" * 999 + "R" + "F" * 999 + "R")
    simulator.run()
    assert not simulator.crashed_cars
    assert simulator.completed_cars[(0, 0)] == ("Koensigg CCXR", 0)
    assert simulator.completed_cars[(999, 0)] == ("Pagani Zonda", 270)

    # Scenario 4:
    # grid: 1000 x 1000
    # car: Lamborghini Superveloce init_pos 0, 0 direction: "E" Full map traversal
    # Results: end at 0, 999 No crashes
    instructions = []
    for i in range(1_000):
        if not i % 2:
            instructions.append("F" * 999 + "LFL")
        else:
            instructions.append("F" * 999 + "RFR")
    simulator.add("Lamborghini Superveloce", (0, 0), "E", "".join(instructions))
    simulator.run()
    assert not simulator.crashed_cars
    assert simulator.completed_cars[(0, 999)] == ("Lamborghini Superveloce", 90)

    # Scenario 5:
    # grid: 1000 x 1000
    # car: Koensigg CCXR init_pos: 0, 0 direction: N Going straight and turning right
    # car: Pagani Zonda init_pos: 999, 999 direction: S Going straight and turning right
    # results: both should NOT crash
    simulator.add("Koensigg CCXR", (0, 0), "N",
                  "F" * 499 + "R" + "F" * 999)
    simulator.add("Pagani Zonda", (999, 999), "S",
                  "F" * 499 + "R" + "F" * 999)
    simulator.run()
    assert not simulator.crashed_cars
    assert simulator.completed_cars[(999, 499)] == ("Koensigg CCXR", 90)
    assert simulator.completed_cars[(0, 500)] == ("Pagani Zonda", 270)

    # Scenario 6:
    # grid: 1000 x 1000
    # car: Koensigg CCXR init_pos: 0, 0 direction: N Going straight and turning right
    # car: Pagani Zonda init_pos: 999, 999 direction: S Going straight and turning right
    # results: both should crash
    simulator.add("Koensigg CCXR", (0, 0), "N",
                  "F" * 499 + "R" + "F" * 999)
    simulator.add("Pagani Zonda", (999, 999), "S",
                  "F" * 500 + "R" + "F" * 999)
    simulator.run()
    assert not simulator.completed_cars
    assert simulator.crashed_cars[(500, 499)] == [("Koensigg CCXR", 1_000), ("Pagani Zonda", 1_000)]


if __name__ == "__main__":
    main()
