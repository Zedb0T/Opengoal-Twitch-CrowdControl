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
IF /I "%AREYOUSURE%" NEQ "Y" GOTO install
pip install asyncio
:install