#!/bin/zsh
source ./.venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install ./package.deployment/openastro-1.1.57.tar.gz
python -m pip install prettytable
python -m pip install requests
