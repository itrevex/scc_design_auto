REM py -3.7-64 -m pip install pandas
REM py -3.7-64 -m pip install Pillow
REM py -3.7-64 -m pip install -U matplotlib
REM py -3.7-64 main.py "input/kap_al_jouf.json"
REM py -3.7-64 plot/trial.py 
REM py -3.7-64 -m PyInstaller main.py
py -3.7-64 -m PyInstaller main.spec

