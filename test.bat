@echo off
REM py -3.7-64 -m  pytest --cov=src/common tests/ --cov-report html
REM py -3.7-64 -m coverage run -m main.py "input/philip.trad"
REM py -3.7-64 -m pytest --help
REM py -3.7-64 -m pytest --cov-report html  
REM py -3.7-64 -m coverage run --source=/src/common/*.py
REM py -3.7-64 -m pytest  src/tests/test_dxf -v
REM py -3.7-64 -m pytest -s -v 
REM py -3.7-64 -m pytest -v
REM py -3.7-64 -m pytest --cov=src/dxf  src/tests/ --cov-report html
py -3.7-64 -m pytest -s -v -k"test_loading_region_lines_for_negative_direction2"
REM py -3.7-64 -m pytest -s -v -k "Nodes" 
REM py -3.7-64 -m coverage html 


