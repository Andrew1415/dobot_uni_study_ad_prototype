## Installation
1. Clone this repository `git clone https://github.com/np425/pi-dobot-gui`
2. Create desktop icon that runs the application **in cloned directory** `bash install.sh`

## Development
1. Clone this repository `git clone https://github.com/np425/pi-dobot-gui`
2. Set up and load python virtual environment `python -m venv venv`, then load it via `venv\Scripts\activate` for Windows, or `venv/bin/activate` for Linux (more in https://docs.python.org/3/library/venv.html)
3. Install required libraries `pip install -r requirements.txt`; Tkinter requires additional package on Linux `tk`: `sudo apt-get install tk`
4. To run `python src/gui.py`