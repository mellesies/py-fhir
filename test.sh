#!/bin/bash

# Make sure the logs directory exists.
mkdir -p logs

# (re)run the unit tests everytime a python source file changes.  
find ./ -name "*.py" | entr sh -c "clear && ./utest.py"
