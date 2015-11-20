#!/bin/bash
cd seed/
sudo docker build -t thedhbox/seed:latest .
cd ../wp-seed/
sudo docker build -t twordpress .

