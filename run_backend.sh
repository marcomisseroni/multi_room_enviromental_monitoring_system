echo "----------------------Welcome to the IoT project backend----------------------" 
echo "Author: Marco Misseroni"

# activate influxdb via docker
docker start influxdb

# activate grafana
sudo systemctl start grafana-server

# open grafana UI
echo "Opening grafana dashboard"
xdg-open http://localhost:3000/d/adml8zm/iot-project?orgId=1&from=now-5m&to=now&timezone=browser