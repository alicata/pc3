call conda activate m3
set PC3_FILEPATH=%1
set P3_MESHPATH=%2
set PC3_ROOT=/tmp/pc3
#cd %PC3_ROOT%
python %PC3_ROOT%/tools/pc3_app.py --samples 0 -vs yes
