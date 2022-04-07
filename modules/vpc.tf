resource "aws_vpc" "unbrickable-vpc" {
    cidr_block = "10.10.0.0/16"
    enable_dns_hostnames = true
    tags = {
        Name = "unbrickable-vpc"
    }
}

resource "aws_security_group" "unbrickable-db-sg" {
  name = "allow-db-access"
  description = "Allow Postgres traffic"
  vpc_id = aws_vpc.unbrickable-vpc.id

  ingress {
      description = "Allow Postgres Access"
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
  availability_zone = "eu-central-1a"

  tags = {
      Name = "unbrickable-private-subnet"
  }
}

resource "aws_subnet" "unbrickable-public-subnet" {
  vpc_id = aws_vpc.unbrickable-vpc.id
  cidr_block = "10.10.2.0/24"
  availability_zone = "eu-central-1b"

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
  availability_zone = aws_subnet.unbrickable-private-subnet.availability_zone
  db_subnet_group_name = aws_db_subnet_group.unbrickable-subnets.name
  vpc_security_group_ids = [aws_security_group.unbrickable-db-sg.id]
  publicly_accessible = true
  name = var.db_name
  username = var.db_user
  password = var.db_password
}

resource "aws_internet_gateway" "unbrickable-gw" {
  vpc_id = aws_vpc.unbrickable-vpc.id
}

resource "aws_route_table" "unbrickable_route_table" {
  vpc_id = aws_vpc.unbrickable-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.unbrickable-gw.id
  }
}