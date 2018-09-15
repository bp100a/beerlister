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
rd /q /s "%WORKSPACE%\lambda_deploy\requests_mock"
rd /q /s "%WORKSPACE%\lambda_deploy\requests_mock-1.5.0.dist-info"
rd /q /s "%WORKSPACE%\lambda_deploy\astroid"
rd /q /s "%WORKSPACE%\lambda_deploy\astroid-2.0.4.dist-info"
rd /q /s "%WORKSPACE%\lambda_deploy\coverage"
rd /q /s "%WORKSPACE%\lambda_deploy\coverage-4.5.1.dist-info"
rd /q /s "%WORKSPACE%\lambda_deploy\colorama"
rd /q /s "%WORKSPACE%\lambda_deploy\colorama-0.3.9.dist-info"
rd /q /s "%WORKSPACE%\lambda_deploy\httplib2"
rd /q /s "%WORKSPACE%\lambda_deploy\httplib2-0.11.3.dist-info"
rd /q /s "%WORKSPACE%\lambda_deploy\lazy_object_proxy"
rd /q /s "%WORKSPACE%\lambda_deploy\lazy_object_proxy-1.3.1.dist-info"
rd /q /s "%WORKSPACE%\lambda_deploy\pip"
rd /q /s "%WORKSPACE%\lambda_deploy\pip-18.0.dist-info"
rd /q /s "%WORKSPACE%\lambda_deploy\aws-cli"

:: some miscellaneous cleanup
rm /q "%WORKSPACE%\lambda_deploy\*.pyd"
rd /q /s "%WORKSPACE%\lambda_deploy\__pycache__"

:: Copy over code modules
xcopy /s /y "%WORKSPACE%\controllers\*.*" "%WORKSPACE%\lambda_deploy\controllers\"
xcopy /s /y "%WORKSPACE%\models\*.*" "%WORKSPACE%\lambda_deploy\models\"
copy /y "%WORKSPACE%\*.py" "%WORKSPACE%\lambda_deploy\"
copy /y "%WORKSPACE%\requirements.txt" "%WORKSPACE%\lambda_deploy\requirements.txt"

:: Now zip it all up
set ZIP_PROG=c:\Program Files\7-Zip\7z.exe

:: Clean out pre-eixsting if any
del /q "%WORKSPACE%\lambda_deploy\taplist.zip"

:: Generate our deployment package
"%ZIP_PROG%" a -r "%WORKSPACE%\lambda_deploy\taplist.zip" "%WORKSPACE%\lambda_deploy\*.*"

:: now push it up to the AWS
aws lambda update-function-code --function-name TapList --region us-east-1 --zip-file fileb://lambda_deploy/taplist.zip