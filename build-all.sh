#!/bin/bash
cd seed/
sudo docker build -t thedhbox/seed:latest .
cd ../lamp-seed/
sudo docker build -t thedhbox/tlamp .
cd ../wp-seed/
sudo docker build -t thedhbox/twordpress .
