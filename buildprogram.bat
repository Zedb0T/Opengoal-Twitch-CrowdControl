:PROMPT
SET /P AREYOUSURE=Install pyinstaller (Y/[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO dotenv
pip install -U pyinstaller
:dotenv
SET /P AREYOUSURE=Install dotenv (Y/[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO ahk
pip install python-dotenv
:ahk
SET /P AREYOUSURE=Install ahk (Y/[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO asyncio
pip install ahk
:asyncio
SET /P AREYOUSURE=Install asyncio (Y/[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO asyncio
pip install asyncio
set mypath=%~dp0
pyinstaller --onefile resources\twitchcommands.py --add-data "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\Lib\site-packages\ahk";ahk --icon resources\appicon.ico 
move "%mypath%dist\twitchcommands.exe" "%mypath%/"
move "%mypath%\twitchcommands.spec" "%mypath%/resources"
RENAME "%mypath%twitchcommands.exe" "RENAMEANDPUTNEAROPENGOAL.exe"
@RD /S /Q "%mypath%/build"
@RD /S /Q "%mypath%/dist"
DEL /S /Q "%mypath%/twitchcommands.exe"
