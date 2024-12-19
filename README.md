#EC2
sudo apt update -y
sudo apt install python3-pip git docker.io docker-compose -y
sudo usermod -aG docker $USER  # Add your user to the Docker group
