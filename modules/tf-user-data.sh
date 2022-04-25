#!/bin/bash
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
docker pull dominikfranzen/unbrickable-webapp:latest
docker run -d -p 80:5000 dominikfranzen/unbrickable-webapp:latest