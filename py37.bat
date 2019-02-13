REM py -3.7-64 -m pip install pandas
REM py -3.7-64 -m pip install Pillow
REM py -3.7-64 -m pip install -U matplotlib
REM py -3.7-64 -m PyInstaller main.py
REM py -3.7-64 -m PyInstaller main.spec
REM git remote add backup "C:\Users\treve\Dropbox\projects\gen_desc"
REM git config --local --bool core.bare false
REM py -3.7-64 plot/trial.py 
py -3.7-64 main.py "input/kap_al_jouf.json"
