#!/bin/bash
# Venv
python3 -m venv venv
. ./venv/bin/activate
pip3 install -r requirements.txt
# Make run.sh executable
sudo chmod u+x run.sh