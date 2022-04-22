#!/bin/bash
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
sudo yum update -y
aws s3 cp s3://unbrickable-data/web-app.zip /home/ec2-user/web-app.zip
cd /home/ec2-user/
unzip web-app.zip
rm web-app.zip
chown -R ec2-user .
#sudo python3 -m venv venv
#sudo . venv/bin/activate
sudo pip3 install Flask
sudo pip3 install sqlalchemy
sudo pip3 install pymysql
export FLASK_APP=app
export FLASK_ENV=venv
cd webserver
sudo python3 app.py