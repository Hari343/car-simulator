from simulator import Simulator
from views import StartMenuView, MainMenuView, AddCarView, ListCarView, ResultsView, StartOverView, GoodbyeView
from copy import deepcopy


class App:
    def __init__(self):
        self.simulator = Simulator()

    def run(self):
        while 1:
            self.simulator.grid_x, self.simulator.grid_y = StartMenuView().render()

            while MainMenuView().render() == 1:
                self.simulator.add(*AddCarView().render())
                ListCarView().render(self.simulator.cars)

            # simulator will clear the car map so
            backup_cars = deepcopy(self.simulator.cars)
            self.simulator.run()
            ListCarView().render(backup_cars)
            ResultsView().render(self.simulator.completed_cars, self.simulator.crashed_cars)

            if StartOverView().render() == 1:
                continue
            else:
                GoodbyeView().render()
                break
