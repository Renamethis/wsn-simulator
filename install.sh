#!/bin/bash
# Venv
python3 -m venv venv
. ./venv/bin/activate
pip3 install -r requirements.txt
# Install ns-3
git clone https://github.com/nsnam/ns-3-dev-git.git
cd ns-3-dev-git
./ns3 configure --enable-examples
venv/bin/python ./waf configure
./waf shell