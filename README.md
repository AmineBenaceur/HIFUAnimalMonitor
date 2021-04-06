# HIFUAnimalMonitor

## Overview
#### A Temperature controlled animal bed with heart rate and temperature monitoring.
#### This project features an LCD screen application with button user-input, it reads sensor data from 3 sensors, displays the live data and transmits it over a TCP server.
#### The temperature control can be set through the buttons or remotely from a client, which uses a P.I.D Controller to output different Duty Cycles to the current driver for resistive heating control.  

## Software
#### source code for P.I.D process, LCD screen, Communicating with the Arduino and the interactive APP are implemented in Python.
#### Source code for reading sensor data and writing it to serial is implemented in C and C++. All are provided as described below:  

## Directory Layout
```
.
├── doc/                   # Documentation files (alternatively `doc`)  
│   ├── README_SETUP.md           # Step by step Arudino, raspberypi and environment installation.
│   ├── README_HW_SETUP.md        # Documentation of electrical and Materials Construction.
|   └──
├── src/
|   ├── capstonepi/        # source code running on the pi.
|   |   ├── constants.yaml        # a Configuration file with P.I.D constants and application settings.  
|   |   ├── MonitorController.py  # our 'main' Class, which instantiates the rest, starts the server and handles app logic.  
|   |   ├── MonitorPID.py         # A threaded class responsible for running the P.I.D process and controlling the bed temp.
|   |   ├── MonitorPID.py         # A threaded class responsible for running the P.I.D process and controlling the bed temp.
|   |   ├── Wiki_PID.py           # P.I.D controls specific library.
|   |   ├── MonitorServer.py      # Server class for communicating with the clients and broadcasting readings.
|   |   ├── HardwareSensors.py    # A threaded class responsible for communication with the Arduino to retrieve sensor readings continously.
|   |   └──
|   ├── Arduino/           # source code running on the Arduino.
|   |   ├── communicate.ino       # Arduino Code for reading the sensor data and writing it to serial.
|   |   ├── libraries/            # Arduino sensor libs.
|   |   └──
|   ├── calibration        # code used for P.I.D calibration and analysis, as well as heating-system logs directory.
|   |   ├── plot_test.py          # a plotting tool used for heating system analysis
|   |   ├── test_logs/            # a directory where P.I.D process test logs are stored if `save_logs` is set to true in constants.yaml
|   |   └──
|   ├── client/            # Client GUI and
|   |   ├── MonitorClient.py             # Client file for interacting with MonitorServer.py
|   |   ├── Widget_AnimalMonitor.py      # Client GUI python example, can be used as an example for building similiar GUIs within applications.
|   |   └──
├── setup.py               # setup file
└──
```

## Maintainers:
  - Amine Benaceur, Project Manager ( Contact: abenaceur12@gmail.com )

## Developers:
  - Amine Benaceur
  - Ryan Ward
  - Farhad Alishov
