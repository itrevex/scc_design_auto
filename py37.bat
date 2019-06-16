@echo off
REM py -3.7-64 -m pip install pandas
REM py -3.7-64 -m pip install Pillow
REM py -3.7-64 -m pip install sympy
REM py -3.7-64 -m pip install -U matplotlib
REM py -3.7-64 -m PyInstaller main.py
REM git remote add backup "C:\Users\treve\Dropbox\projects\gen_desc"
REM git config --local --bool core.bare false
REM py -3.7-64 plot/trial.py 

REM py -3.7-64 -m PyInstaller src/main.py

REM compile code
REM py -3.7-64 -m PyInstaller main.spec
REM iscc "setup/design_auto.iss"
REM "setup/setups/ssc_design_setup-1.0.9"

REM "dist/main/trsc"
REM py -3.7-64 -m pip freeze rem show all packages installed
REM git rm --cached *.exe 
REM py -3.7-64 src/main.py "../project/project.json"
py -3.7-64 src/main.py "../project/actual.json"

REM py -3.7-64 -m pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
REM py -3.7-64 -m pip freeze > requirements.txt
REM ./trsc.exe ../../project/project.json