#!/bin/bash

export PATH=$PWD/python/bin:$PATH
export PYTHONPATH=$PWD/packages
export HOME=$PWD

python3 convert_data.py "$1"