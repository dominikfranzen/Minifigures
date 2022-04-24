resource "aws_vpc" "unbrickable-vpc" {
    cidr_block = "10.10.0.0/16"
    enable_dns_hostnames = true
    tags = {
        Name = "unbrickable-vpc"
    }
}

resource "aws_security_group" "unbrickable-webserver-sg" {
  name = "allow-website-access"
  description = "Open ports for http and ssh connection"
  vpc_id = aws_vpc.unbrickable-vpc.id

  ingress {
      description = "Allow HTTP access"
      from_port = 80
      to_port = 80
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }
    ingress {
      description = "Allow SSH access"
      from_port = 22
      to_port = 22
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
      from_port = 0
      to_port = 0
      protocol = "-1"
      cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "unbrickable-db-sg" {
  name = "allow-db-access"
  description = "Allow MariaDB traffic"
  vpc_id = aws_vpc.unbrickable-vpc.id

  ingress {
      description = "Allow MariaDB Access"
      from_port = 3306
      to_port = 3306
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
      from_port = 0
      to_port = 0
      protocol = "-1"
      cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_subnet" "unbrickable-private-subnet" {
  vpc_id = aws_vpc.unbrickable-vpc.id
  cidr_block = "10.10.1.0/24"
  availability_zone = "eu-central-1b"

  tags = {
      Name = "unbrickable-private-subnet"
  }
}

resource "aws_subnet" "unbrickable-public-subnet" {
  vpc_id = aws_vpc.unbrickable-vpc.id
  cidr_block = "10.10.2.0/24"
  availability_zone = "eu-central-1a"

  tags = {
      Name = "unbrickable-public-subnet"
  }
}

resource "aws_db_subnet_group" "unbrickable-subnets" {
  name = "unbrickable-subnets"
  subnet_ids = [aws_subnet.unbrickable-private-subnet.id, aws_subnet.unbrickable-public-subnet.id]
  tags = {
      Name = "unbrickable-subnets"
  }
}

resource "aws_db_instance" "unbrickable-db" {
  identifier = "unbrickable"
  instance_class = "db.t3.micro"
  allocated_storage = 20
  engine = "mariadb"
  engine_version = "10.5.13"
  availability_zone = aws_subnet.unbrickable-public-subnet.availability_zone
  db_subnet_group_name = aws_db_subnet_group.unbrickable-subnets.name
  vpc_security_group_ids = [aws_security_group.unbrickable-db-sg.id]
  publicly_accessible = true
  name = var.db_name
  username = var.db_user
  password = var.db_password
  skip_final_snapshot = true
}

resource "aws_s3_bucket" "unbrickable-data" {
  bucket = "unbrickable-data"

  tags = {
    Name        = "Unbrickable data"
  }
}

resource "aws_s3_bucket_object" "web-app" {
  bucket = aws_s3_bucket.unbrickable-data.id
  key    = "web-app.zip"
  acl    = "private"  # or can be "public-read"
  source = "web-app.zip"
  etag = filemd5("web-app.zip")
}

resource "aws_internet_gateway" "unbrickable-gw" {
  vpc_id = aws_vpc.unbrickable-vpc.id
}

resource "aws_key_pair" "webserver-ssh" {
    key_name = "webserver-ssh-key"
    public_key = var.ssh-key
}

resource "aws_iam_role" "web-iam-role" {
    name = "web-iam-role"
    assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_instance_profile" "web-instance-profile" {
    name = "web-instance-profile"
    role = "web-iam-role"
}

resource "aws_iam_role_policy" "web-iam-role-policy" {
  name = "web-iam-role-policy"
  role = "${aws_iam_role.web-iam-role.id}"
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*",
                "s3-object-lambda:*"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_instance" "webserver" {
  ami = "ami-01d9d7f15bbea00b7"
  instance_type = "t2.micro"
  availability_zone = "eu-central-1a"
  key_name = aws_key_pair.webserver-ssh.key_name
  security_groups = [aws_security_group.unbrickable-webserver-sg.id]
  subnet_id = aws_subnet.unbrickable-public-subnet.id
  iam_instance_profile = "${aws_iam_instance_profile.web-instance-profile.id}"

  user_data = "${file("modules/tf-user-data.sh")}"
}

resource "aws_eip" "webserver" {
  instance = aws_instance.webserver.id
  vpc      = true
}

resource "aws_route_table" "unbrickable_route_table" {
  vpc_id = aws_vpc.unbrickable-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.unbrickable-gw.id
  }
}

resource "aws_route_table_association" "public_subnet" {
  subnet_id = aws_subnet.unbrickable-public-subnet.id
  route_table_id =aws_route_table.unbrickable_route_table.id  
}