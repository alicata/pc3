call conda activate m3
set PC3_ROOT=/tmp/pc3
set PC3_FILEPATH=%1
python %PC3_ROOT%/tools/pc3_app.py --samples 0 -vs yes
