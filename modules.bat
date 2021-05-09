@echo off


:start
cls

set python_ver=38

python ./get-pip.py

cd \
cd \python%python_ver%\Scripts\
pip install torch
pip install matplotlib
pip install pygame

pause
exit