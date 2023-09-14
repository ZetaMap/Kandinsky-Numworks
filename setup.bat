@echo off
:: Just clean build files if '-c' argument is present
if "%~1"=="-c" ( set JUST_CLEAN=true ) else set JUST_CLEAN=false

:: Remove previous build files
call :clean
if %JUST_CLEAN% == true exit /b 0
:: Check and install build dependencies
echo.
echo Installing build dependencies ...
pip install -U build
:: Build module
echo.
echo Building library ...
python -m build
:: Ask install
echo.
call :ask "Install library" || pip install .
:: Ask clear files
echo.
call :ask "Clear setup files" 1 || call :clean
:: Re-change library version to 'null'
python setup.py --version-null
:: Finished
echo All done
exit /b 0

:: Somes methods
:ask
  if "%~1" == "" (
    echo ask: a question must be specified
    exit /b 1
  )
  if "%~2" == "1" ( 
    set default=Y/n
  ) else set default=y/N

  set choise=
  set /p choise=%~1? [%default%]: 
  if "%choise%" == "y" exit /b 1
  if "%choise%" == "yes" exit /b 1
  if "%choise%" == "" ( if "%~2" == "1" exit /b 1 )
  exit /b 0

:clean
  echo Cleaning build files ...
  rd /s /q build src\kandinsky.egg-info 2> nul
  if exist dist (
    dir /b /a "dist" | findstr .>nul && (
      call :ask "'dist' folder not empty, remove" || rd /s /q dist 
      exit /b 0
    )
    rd /s /q dist 
  )
  exit /b 0
