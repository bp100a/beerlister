:: Create a deployment package
@echo on
setlocal ENABLEEXTENSIONS

if NOT DEFINED WORKSPACE set WORKSPACE=d:\Program Files (x86)\Jenkins\workspace

:: If deployment folder does not exist - create it!
if not exist "%WORKSPACE%\lambda_deploy" mkdir "%WORKSPACE%\lambda_deploy"

:: Clean out any previous data from deployment folder
rd /q /s lambda_deploy

:: Copy all the relevant site packages
copy /s "%WORKSPACE%\pyenv\Lib\site-packages\*.*" "%WORKSPACE%\lambda_deploy"

:: Remove testing packages
rd /q /s "%WORKSPACE%\lambda_deploy\nose*"
rd /q /s "%WORKSPACE%\lambda_deploy\nosexcover*"
rd /q /s "%WORKSPACE%\lambda_deploy\pylint*"



