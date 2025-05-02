#!/usr/bin/bash 
echo "Setting up virtual environment..."
python3 -m venv ./venv
. ./venv/bin/activate
pip install --upgrade pip
pip install -r ./service/requirements.txt
echo "Done!"
