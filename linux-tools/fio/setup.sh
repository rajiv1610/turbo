#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Update sources for installing tools
echo "" >> /etc/apt/sources.list
echo "deb http://us.archive.ubuntu.com/ubuntu vivid main universe" >> /etc/apt/sources.list 

# Install tools
apt-get update
apt-get install -y fio
apt-get install -y bwm-ng
apt-get install -y iotop
apt-get install -y screen

echo ""
echo "This machine has been setup to run ./benchmark.sh"
echo ""
