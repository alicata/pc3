:: setup env for pc3 engine 
set PC3_HOME=%CD%

setx PATH "%PATH%;%PC3_HOME%"
setx PYTHONPATH "%PYTHONPATH%;%PC3_HOME%"
echo pc3 engine added to env path

:: engine dependencies
pip install -r requirements.txt
 