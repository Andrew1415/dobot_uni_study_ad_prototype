#!/bin/bash

root_dir=$(dirname "$0")

echo "Changing directory to project root"
cd $(echo $root_dir)

echo "Loading virtual environment"
source venv/bin/activate

echo "Running program"
python src/gui.py