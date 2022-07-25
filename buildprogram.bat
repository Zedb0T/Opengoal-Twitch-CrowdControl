set mypath=%~dp0
pyinstaller --onefile twitchcommands.py --add-data "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\Lib\site-packages\ahk";ahk --icon appicon.ico 
move "%mypath%dist\twitchcommands.exe" "%mypath%/"
RENAME "%mypath%twitchcommands.exe" "RENAMEANDPUTNEAROPENGOAL.exe"