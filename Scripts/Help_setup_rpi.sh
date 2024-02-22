#!/bin/bash

#####################################################################
#	Functions
#####################################################################

#********************#
# Install bonjour    #
#********************#
install_bonjour()
{
    sudo apt update

    sudo apt install libnss-mdns

    sudo nano /etc/hostname

    echo "Don't forget to reboot !"
}

#####################################################################
#	Calls
#####################################################################
install_bonjour
