# Candy Robot GUI

Candy Robot project uses a robotic hand to pick up a user-selected candy from fixated slots on a surface and dropping them in user's hands. Purpose of the project is to attract new students to the university. 

This project consists of 3 parts:
1. [Graphical user interface implemented in Raspberry PI.](https://github.com/np425/pi-dobot-gui)
2. [Candy physical movement implemented with Dobot robotic hand.](https://github.com/aidasgau/dobotmg400-candypicker)
3. Electrical wiring connecting both components and providing communication.

This github repository covers the _first part_ of this project.

## Logic
![Raspberry Flow Diagram](doc/Candy_Raspberry_Flow_Diagram.drawio.svg)

GPIO Pins used for the project:
- Out 35 for candy 1 selection
- Out 37 for candy 2 selection
- In 33 for candy drop off feedback signal (synchronisation)

## Setup 
1. Clone this repository `git clone https://github.com/np425/pi-dobot-gui` and move into it `cd pi-dobot-gui`
2. Rename `questions.json.example` to `questions.json` and replace contents with custom quiz questions.
3. If necessary update pins in `src/communication.py`

## Installation
1. Install desktop icon that runs the application `bash install.sh`

## Development
1. Set up and load python virtual environment `python -m venv venv`, then load it via `venv\Scripts\activate` for Windows, or `venv/bin/activate` for Linux (more in https://docs.python.org/3/library/venv.html)
2. Install required libraries `pip install -r requirements.txt`; Tkinter requires additional package on Linux `tk`: `sudo apt-get install tk`
3. To run `python run.py`

## Configuration
- Pin configuration can be changed in file `src/communication.py`
- Quiz question bank can be changed in file `questions.json`
