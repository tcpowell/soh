@echo off


REM Check for Games dir
echo Checking for %USERPROFILE%\Games
if not exist "%USERPROFILE%\Games" mkdir %USERPROFILE%\Games


REM Git pull
git fetch --all
git reset --hard origin/master





REM Check for latest zip
REM Check for existing installs
REM Download latest
REM 
REM 
REM 
REM 
REM 
REM 
REM 
REM 
REM 
REM 
REM 
REM 
REM 
REM 
REM 
REM 

pause
