# car-simulator

This is a simulation application for simulating cars driving in a grid. 

**Running the application**

*Note: Prebuilt binaries for Windows 11 (x86-64) available in the dist folder. Simply double-click
the car-simulator.exe in dist/car-simulator/ to start the application. To build the application yourself 
refer the "Building the application" section below.*

Create a python venv and activate it

Windows:

```commandline
python -m venv venv
venv\Scripts\activate
```

Linux: 

```bash
python -m venv venv
source venv/bin/activate
```
Then install the requirements. Please see the Dependencies section for the required external 
dependencies. *Note: This application doesn't require any dependencies for running in CLI mode.*

```commandline
pip install -r requirements.txt
```
Simply run the following command to start the application:

```commandline
python main.py
```
If you want to start the application in CLI mode, run:

```commandline
python cli.py
```

**Building the application**

This project uses Pyinstaller to build the app. It should automatically install when 
you install the requirements. Be aware that pyinstaller requires some additional 
dependencies in the Linux platform. Refer the official Pyinstaller documentation if 
you run into any issues. 

To build the app, simply run

```commandline
pyinstalller main.py -n car-simulator -w
```

**Dependencies**
1. Customtkinter: To provide a reasonably modern looking UI (standard tkinter is atrocious)
2. Pyinstaller: For building
