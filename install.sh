#!/bin/bash

root_dir=$(dirname "$0")

echo "Changing directory to project root"
cd $(echo $root_dir)

echo "Setting up virtual environment"
if [ ! -d venv/ ]; then
    python -m venv venv
fi

echo "Activating virtual environment"
source venv/bin/activate

echo "Installing required libraries"
pip install -r requirements.txt

dpkg -s tk > /dev/null
if [ $? -ne 0 ]; then
    sudo apt-get install tk
fi

echo "Installing executable"
sudo ln run.sh /usr/local/bin/saldainiai

echo "Installing desktop icon"
cp install/saldainiai.desktop ~/Desktop/