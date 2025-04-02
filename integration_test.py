from runner import Runner
from views import StartMenuView, StartOverView, MainMenuView, AddCarView, ListCarView, ResultsView, GoodbyeView

_app_command = "python app.py"


def _verify_output(runner: Runner, content: str):
    output = runner.read(len(content))
    assert output == content


"""
    Journey 1: This is the standard user journey. The user initializes the app, gives correct inputs and adds a car 
    then runs the simulation. Then stops the app.
"""


def journey_1():
    print("Running user journey 1")
    with Runner(_app_command) as runner:
        # verify start menu prompt
        _verify_output(runner, StartMenuView().content)
        # set grid size as 10 x 10
        runner.write("10 10")

        # verify main menu prompt
        _verify_output(runner, MainMenuView().content)

        # Select add car
        runner.write("1")

        # verify add car name prompt
        _verify_output(runner, "Please enter the name of the car: ")

        # add car name
        runner.write("sample_car")

        # verify car pos prompt
        _verify_output(runner, "Please enter the initial pos of the car in x y direction format: ")

        # add car pos and direction
        runner.write("5 5 E")

        # verify car commands prompt
        _verify_output(runner, "Please enter the commands for the car: ")

        # add some commands
        runner.write("FFRLRRRRRLLLLRR")

        # verify list cars prompt
        _verify_output(runner, "Your current list of cars are: \n")
        _verify_output(runner, "- sample_car, (5, 5) E, FFRLRRRRRLLLLRR\n")

        # verify main menu prompt again
        _verify_output(runner, MainMenuView().content)

        # select run simulation
        runner.write("2")

        # verify list cars again
        _verify_output(runner, "Your current list of cars are: \n")
        _verify_output(runner, "- sample_car, (5, 5) E, FFRLRRRRRLLLLRR\n")

        # verify results view
        _verify_output(runner, "Simulation Results\n \nCompleted Cars: \n")
        _verify_output(runner, "- sample_car, (7, 5) N\n \n")

        # verify start over view
        _verify_output(runner, StartOverView().content)

        runner.write("2")

        # verify goodbye view
        _verify_output(runner, GoodbyeView().content)

    print("User journey 1 is successful")


"""
    Journey 2: This is a user journey with wrong inputs, crashed cars and start over
"""


def journey_2():
    print("Running user journey 2")
    with Runner(_app_command) as runner:
        # verify start menu prompt
        _verify_output(runner, StartMenuView().content)
        # set grid size as 10 x 10 (wrong input)
        runner.write("10 x 10")

        # verify the user error prompt
        _verify_output(runner, "Invalid input. The input should be in 'x y' format\n")

        # verify the start menu again
        _verify_output(runner, StartMenuView().content)
        # set grid size as 10 x 10
        runner.write("10 10")

        # verify main menu prompt
        _verify_output(runner, MainMenuView().content)

        # Select add car
        runner.write("1")

        # verify add car name prompt
        _verify_output(runner, "Please enter the name of the car: ")

        # add car name
        runner.write("sample_car")

        # verify car pos prompt
        _verify_output(runner, "Please enter the initial pos of the car in x y direction format: ")

        # add car pos and direction - wrong input
        runner.write("5, 5 E")

        # verify error prompt
        _verify_output(runner, "Invalid input. x, y both should be integers\n")

        # again add car name prompt
        _verify_output(runner, "Please enter the name of the car: ")
        runner.write("sample_car")

        # verify car pos prompt
        _verify_output(runner, "Please enter the initial pos of the car in x y direction format: ")

        # add car pos and direction
        runner.write("1 2 N")

        # verify car commands prompt
        _verify_output(runner, "Please enter the commands for the car: ")

        # add some commands
        runner.write("FFRFFFFRRL")

        # verify list cars prompt
        _verify_output(runner, "Your current list of cars are: \n")
        _verify_output(runner, "- sample_car, (1, 2) N, FFRFFFFRRL\n")

        # verify main menu prompt again
        _verify_output(runner, MainMenuView().content)

        # add second car
        runner.write("1")

        # verify add car name prompt
        _verify_output(runner, "Please enter the name of the car: ")

        # add car name
        runner.write("sample_car2")

        # verify car pos prompt
        _verify_output(runner, "Please enter the initial pos of the car in x y direction format: ")

        # add car pos and direction
        runner.write("7 8 W")

        # verify car commands prompt
        _verify_output(runner, "Please enter the commands for the car: ")

        # add some commands
        runner.write("FFLFFFFFFF")

        # verify list cars prompt
        _verify_output(runner, "Your current list of cars are: \n")
        _verify_output(runner, "- sample_car, (1, 2) N, FFRFFFFRRL\n")
        _verify_output(runner, "- sample_car2, (7, 8) W, FFLFFFFFFF\n")

        # verify main menu prompt again
        _verify_output(runner, MainMenuView().content)

        # select run simulation
        runner.write("2")

        # verify list cars again
        _verify_output(runner, "Your current list of cars are: \n")
        _verify_output(runner, "- sample_car, (1, 2) N, FFRFFFFRRL\n")
        _verify_output(runner, "- sample_car2, (7, 8) W, FFLFFFFFFF\n")

        # verify results view
        _verify_output(runner, "Simulation Results\n \nCompleted Cars: \n \n")
        _verify_output(runner, "Crashed Cars: \n")
        _verify_output(runner, "- sample_car crashed at (5, 4) on step 7 with car / cars: ['sample_car2']\n")
        _verify_output(runner, "- sample_car2 crashed at (5, 4) on step 7 with car / cars: ['sample_car']\n")

        # verify start over view
        _verify_output(runner, StartOverView().content)

        # starting over
        runner.write("1")

        # verify start menu prompt
        _verify_output(runner, StartMenuView().content)
    print("User journey 2 successful")


def main():
    journey_1()
    journey_2()


if __name__ == "__main__":
    main()

