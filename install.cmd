call conda activate o3
set PC3_HOME=D:/g/pc3
pip install pyrr
pip install moderngl
pip install moderngl-window
pip install pywavefront
setx path "%path%;%PC3_HOME%"
echo new path:
echo %PATH%
 