#EC2<br/>
sudo apt update -y<br/>
sudo apt install python3-pip git docker.io docker-compose -y<br/>
sudo usermod -aG docker $USER  # Add your user to the Docker group<br/>
sudo chmod 666 /var/run/docker.sock<br/>

Remember to allow all hosts with console as well as flask app(0.0.0.0)
Map the container port hosting flask app to host port =80
Then use Public IPv4 DNS from AWS console but change https to http
