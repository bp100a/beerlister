:: Create a deployment package
@echo on
setlocal ENABLEEXTENSIONS

if NOT DEFINED WORKSPACE set WORKSPACE=d:\Program Files (x86)\Jenkins\workspace\TapList

echo workspace = "%WORKSPACE%"

:: If deployment folder does exists - clean it out
if exist "%WORKSPACE%\lambda_deploy" rd /q /s lambda_deploy

:: make a new folder since 'rd' removes folder
mkdir "%WORKSPACE%\lambda_deploy"

:: Copy all the relevant site packages
xcopy /s /q "%WORKSPACE%\pyenv\Lib\site-packages\*.*" "%WORKSPACE%\lambda_deploy"

:: Remove testing packages
rd /q /s "%WORKSPACE%\lambda_deploy\nose"
rd /q /s "%WORKSPACE%\lambda_deploy\nose-1.3.7.dist-info"
rd /q /s "%WORKSPACE%\lambda_deploy\nosexcover"
rd /q /s "%WORKSPACE%\lambda_deploy\nosexcover-1.0.11.dist-info"
rd /q /s "%WORKSPACE%\lambda_deploy\pylint"
rd /q /s "%WORKSPACE%\lambda_deploy\pylint-2.1.1.dist-info"

:: Copy over code modules
xcopy /s /y "%WORKSPACE%\controllers\*.*" "%WORKSPACE%\lambda_deploy\controllers\"
xcopy /s /y "%WORKSPACE%\models\*.*" "%WORKSPACE%\lambda_deploy\models\"
copy /y "%WORKSPACE%\*.py" "%WORKSPACE%\lambda_deploy\"
copy /y "%WORKSPACE%\requirements.txt" "%WORKSPACE%\lambda_deploy\requirements.txt"
