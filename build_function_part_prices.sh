#!/bin/bash/
pip3 install --target ./package sqlalchemy
pip3 install --target ./package pymysql
pip3 install --target ./package requests-oauthlib

cd package
zip -r ../lambda-package-part-prices.zip .
cd ..
zip lambda-package-part-prices.zip auth.py auth_credentials.json database_handling.py db_secrets.json save_part_prices.py clustering/categories.json lambda_save_part_prices.py

rm -r package 