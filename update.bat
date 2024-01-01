@echo off


REM Check for Games dir
if not exist "%USERPROFILE%\Games" (
echo Creating directory %USERPROFILE%\Games...
mkdir %USERPROFILE%\Games
)

echo Updating repository


git fetch --all
git reset --hard origin/master





REM Check for latest zip
for /F "tokens=* delims=/" %%i in (soh_list.txt) do (


  if exist "%USERPROFILE%\Games\%%~ni" (
    echo Already on the latest version
  ) else (
  echo New version found: %%~ni
  
  echo Creating directory %USERPROFILE%\Games\%%~ni
  mkdir %USERPROFILE%\Games\%%~ni
  
  echo Downloading zip: %%i
  wget %%i -q -P %TEMP%
  
  echo Extracting zip to %USERPROFILE%\Games\%%~ni
  tar -xf %TEMP%\%%~nxi -C %USERPROFILE%\Games\%%~ni
  
  echo Cleaning up temporary files
  del %TEMP%\%%~nxi
  )



goto :break
)


:break
echo done



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
