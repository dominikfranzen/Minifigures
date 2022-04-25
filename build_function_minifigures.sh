#!/bin/bash/
pip3 install --target ./package sqlalchemy
pip3 install --target ./package pymysql
pip3 install --target ./package requests-oauthlib

cd package
zip -r ../lambda-package-minifigures.zip .
cd ..
zip lambda-package-minifigures.zip auth.py clustering/categories.json auth_credentials.json database_handling.py db_secrets.json save_minifigure_prices.py lambda_save_minifigure_prices.py

rm -r package 