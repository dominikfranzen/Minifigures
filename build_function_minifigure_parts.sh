#!/bin/bash/
pip3 install --target ./package sqlalchemy
pip3 install --target ./package pymysql
pip3 install --target ./package requests-oauthlib

cd package
zip -r ../lambda-package-minifigure-parts.zip .
cd ..
zip lambda-package-minifigure-parts.zip auth.py clustering/categories.json save_parts.py db_secrets.json database_handling.py auth_credentials.json lambda_save_parts.py

rm -r package 