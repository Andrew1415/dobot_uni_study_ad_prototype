#!/bin/bash

root_dir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

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
echo "#!/bin/bash" | sudo tee /usr/local/bin/saldainiai
echo "bash $root_dir/run.sh" | sudo tee --append /usr/local/bin/saldainiai

echo "Installing desktop icon"
cp install/saldainiai.desktop ~/Desktop/