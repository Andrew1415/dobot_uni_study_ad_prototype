#!/bin/bash
# Setup virtual python environment
if [ ! -d venv/ ]; then
    python -m venv venv
fi

# Activate virtual python environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

if [! (dpkg -s tk)]; then
    sudo apt-get install tk
fi

# Install desktop icon
cp install/saldainiai.desktop ~/Desktop/