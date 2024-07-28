set mypath=%~dp0
python -c "import sysconfig; print(sysconfig.get_path('purelib') + '\\ahk')" > tmpFile
set /p PYSITEPKG_DIR= < tmpFile
DEL tmpFile

pyinstaller --onefile resources\twitchcommands.py --add-data "%PYSITEPKG_DIR%:ahk" --icon resources\appicon.ico

move "%mypath%dist\twitchcommands.exe" "%mypath%/"
move "%mypath%\twitchcommands.spec" "%mypath%/resources"
DEL /S /Q "%mypath%Jak1Twitch.backup.exe"
RENAME "%mypath%Jak1Twitch.exe" "Jak1Twitch.backup.exe"
RENAME "%mypath%twitchcommands.exe" "Jak1Twitch.exe"
@RD /S /Q "%mypath%/build"
@RD /S /Q "%mypath%/dist"
DEL /S /Q "%mypath%/twitchcommands.exe"