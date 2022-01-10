call conda activate o3
set PC3_FILEPATH=%1
set P3_MESHPATH=%2
set P3_MASKPATTERN=%3
set PC3_ROOT=d:/g/pc3
python %PC3_ROOT%/tools/pc3_app.py --samples 0 -vs yes
