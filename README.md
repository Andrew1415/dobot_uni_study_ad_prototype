
## Setup 
1. Clone this repository `https://github.com/Andrew1415/dobot_uni_study_ad_prototype.git` and move into it `cd dobot_uni_study_ad_prototype`
2. Rename `questions.json.example` to `questions.json` and replace contents with custom quiz questions.
3. If necessary update pins in `src/communication.py`

## Installation
1. Install desktop icon that runs the application `bash install.sh`

## Development
1. Set up and load python virtual environment `python -m venv venv`, then load it via `venv\Scripts\activate` for Windows, or `venv/bin/activate` for Linux (more in https://docs.python.org/3/library/venv.html)
2. Install required libraries `pip install -r requirements.txt`; Tkinter requires additional package on Linux `tk`: `sudo apt-get install tk`
3. To run `python run.py`

## Configuration
- Quiz question bank can be changed in file `questions.json`
