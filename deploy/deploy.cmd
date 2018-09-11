:: Using the AWS CLI (with credentials pre-loaded) upload the zipfile we created
aws lambda update-fuction-code --function-name TapList --zip-file fileb://../lambda_deploy/taplist.zip
