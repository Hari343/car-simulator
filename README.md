# car-simulator

This is a simulation application for simulating cars driving in a grid. 

**Running the application**

You need Python 3.11 or higher to run the application. The application requires no external dependencies. Simply run the
following command to start the application

Once started you would be asked to input the grid size. Enter the grid size in 'x y' format. For example for a 10 x 10
grid enter 10 10. Then press Enter to show the Main Menu.

Main Menu will have the following options:

1. Add Car
2. Run Simulation

Enter the number of the option and press Enter. For example, to add a car to the simulation, type 1 and press Enter.

When adding a car, you need to provide a car name, car's initial position and the direction it is facing and the
movement commands for the car. Follow onscreen prompts to input this information. Once a car is added, you will be redirected
to the Main Menu. From here you can add another car or start the simulation. 

Once simulation is done results will be displayed. The results will show the cars' position and whether they crashed or not
during the simulation

**Testing**

To run unittest, simply run:

```commandline
python -m unittest
```


To run integration test, run

```commandline
python integration_test.py
```
