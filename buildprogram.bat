
set mypath=%~dp0
pyinstaller --onefile resources\twitchcommands.py --add-data "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\Lib\site-packages\ahk";ahk --icon resources\appicon.ico 
move "%mypath%dist\twitchcommands.exe" "%mypath%/"
move "%mypath%\twitchcommands.spec" "%mypath%/resources"
RENAME "%mypath%twitchcommands.exe" "OPENGOALTWITCHv0.1.exe"
@RD /S /Q "%mypath%/build"
@RD /S /Q "%mypath%/dist"
DEL /S /Q "%mypath%/twitchcommands.exe"
