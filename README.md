#EC2<br/>
sudo apt update -y<br/>
sudo apt install python3-pip git docker.io docker-compose -y<br/>
sudo usermod -aG docker $USER  # Add your user to the Docker group<br/>
sudo chmod 666 /var/run/docker.sock<br/>
