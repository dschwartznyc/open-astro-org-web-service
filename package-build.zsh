#!/bin/zsh
cd ./openastro.package
python3 setup.py sdist
pip install ./dist/openastro-1.1.57.tar.gz
cd ..
cp ./openastro.package/dist/** ./package.deployment/
