#!/bin/bash/
pip3 install --target ./package sqlalchemy pymysql requests-oauthlib

cd package
zip -r ../lambda-package-minifigure-parts.zip .

cd ..
cp lambda-package-minifigure-parts.zip lambda-package-minifigures.zip
cp lambda-package-minifigure-parts.zip lambda-package-part-prices.zip
cp lambda-package-minifigure-parts.zip lambda-package-profit-calculation.zip
zip lambda-package-minifigure-parts.zip auth.py clustering/categories.json save_parts.py db_secrets.json database_handling.py auth_credentials.json lambda_save_parts.py
zip lambda-package-minifigures.zip auth.py clustering/categories.json auth_credentials.json database_handling.py db_secrets.json save_minifigure_prices.py lambda_save_minifigure_prices.py
zip lambda-package-part-prices.zip auth.py auth_credentials.json database_handling.py db_secrets.json save_part_prices.py clustering/categories.json lambda_save_part_prices.py
zip lambda-package-profit-calculation.zip auth.py database_handling.py db_secrets.json profit_calculation.py profit-calculation.sql lambda_profit_calculation.py

rm -r package 