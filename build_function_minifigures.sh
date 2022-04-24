#!/bin/bash/
pip3 install --target ./package sqlalchemy
pip3 install --target ./package pymysql
pip3 install --target ./package requests-oauthlib

cd package
zip -r ../lambda-package-minifigures.zip .
cd ..
zip lambda-package-minifigures.zip auth.py
zip lambda-package-minifigures.zip auth_credentials.json
zip lambda-package-minifigures.zip database_handling.py
zip lambda-package-minifigures.zip db_secrets.json
zip lambda-package-minifigures.zip save_minifigure_prices.py
zip lambda-package-minifigures.zip lambda_save_minifigure_prices.py
zip lambda-package-minifigures.zip clustering/categories.json

rm -r package 