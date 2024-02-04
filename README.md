# Candy Robot GUI

Candy Robot project uses a robotic hand to pick up a user-selected candy from fixated slots on a surface and dropping them in user's hands. Purpose of the project is to attract new students to the university. 

This project consists of 3 parts:
1. Graphical user interface implemented in Raspberry PI.
2. Candy physical movement implemented with Dobot robotic hand.
3. Electrical wiring connecting both components and providing communication.

This github repository covers the first part of this project.

## Logic
![Raspberry Flow Diagram](doc/Candy_Raspberry_Flow_Diagram.drawio.svg)

GPIO Pins used for the project:
- Out 35 for candy "Ananasas" selection
- Out 37 for candy "Ananasas" selection
- In 33 for candy drop off feedback signal (synchronisation)

## Installation
1. Clone this repository `git clone https://github.com/np425/pi-dobot-gui`
2. Create desktop icon that runs the application **in cloned directory** `bash install.sh`

## Development
1. Clone this repository `git clone https://github.com/np425/pi-dobot-gui`
2. Set up and load python virtual environment `python -m venv venv`, then load it via `venv\Scripts\activate` for Windows, or `venv/bin/activate` for Linux (more in https://docs.python.org/3/library/venv.html)
3. Install required libraries `pip install -r requirements.txt`; Tkinter requires additional package on Linux `tk`: `sudo apt-get install tk`
4. To run `python src/gui.py`

## Configuration
- Pin configuration can be changed in file [candy.py](src/candy.py)
- Quiz question bank can be changed in file [question_bank.py](question_bank.py)
