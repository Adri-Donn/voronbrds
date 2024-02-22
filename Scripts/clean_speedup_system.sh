#!/bin/bash
#####################################################################
#	Informations
#####################################################################
#   This script should be run as root.
#   sudo ./clean_speedup_system.sh   
#
#   You may need to make this script executable
#   sudo chmod +x clean_speedup_system.sh

#####################################################################
#	Ensure script is run as root
#####################################################################
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

#####################################################################
#	Repair / optimize packets system
#####################################################################
cp -arf /var/lib/dpkg /var/lib/dpkg.backup
cp /var/lib/dpkg/status-old /var/lib/dpkg/status
cp /var/lib/dpkg/available-old /var/lib/dpkg/available
rm -rf /var/lib/dpkg/updates/*
rm -rf /var/lib/apt/lists
mkdir /var/lib/apt/lists
mkdir /var/lib/apt/lists/partial
apt clean
apt update
dpkg --clear-avail
dpkg --configure -a
apt install -f
apt update
apt dist-upgrade
apt autoclean 

#####################################################################
#	Install dependencies
#####################################################################
apt install deborphan

#####################################################################
#	Cleaning
#####################################################################
apt autoremove
[[ $(dpkg -l | grep ^rc) ]] && dpkg -P $(dpkg -l | awk '/^rc/{print $2}') || echo "No packets to clean"
apt $(deborphan)
apt --autoremove purge $(deborphan)

#####################################################################