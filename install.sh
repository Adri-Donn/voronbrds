#!/bin/bash

####################################################################################################
# Global function definitions
####################################################################################################
# $1 : Source file path and name if file does not exist (From)
# $2 : File path and name (To)
check_file_exists_or_create(){
    if [ ! -f "$2" ]; then
        echo "Creating $2 ..." 
        cp "$1" "$2"
    fi
}

##################################################
# $1 : Source file path and name if file does not exist (From)
# $2 : File path and name (To)
create_symbolic_link()
{
    if [ ! -f "$2" ]; then
        echo "Creating symbolic link : From $1 to $2 ..."
        ln -sf "$1" "$2"

        chmod 755 "$2"
    fi
    
}

####################################################################################################
# Variables
####################################################################################################
SCRIPT_LOCATION=$(cd $(dirname "${BASH_SOURCE:-$0}") && pwd)

KLIPPER_PATH="${HOME}/klipper"
MOONRAKER_PATH="${HOME}/moonraker"
PRINTER_DATA_CONFIG_PATH="${HOME}/printer_data/config"
SYSTEMDDIR="/etc/systemd/system"
PYTHONDIR="${MOONRAKER_VENV:-${HOME}/moonraker-env}"

####################################################################################################
# Force script to exit if an error occurs
####################################################################################################
set -e

####################################################################################################
# Define steps
####################################################################################################
##################################################
# Step : Verify ready
##################################################
# Helper functions
verify_ready()
{
    if [ "$EUID" -eq 0 ]; then
        echo "This script must not run as root"
        exit -1
    fi
}

##################################################
# Step : Verify Klipper has been installed
##################################################
check_klipper()
{
    if [ "$(sudo systemctl list-units --full -all -t service --no-legend | grep -F "klipper.service")" ]; then
        echo "Klipper service found!"
    else
        echo "Klipper service not found, please install Klipper first"
        exit -1
    fi
}

##################################################
# Step : Check dependencies
##################################################
check_dependencies()
{
    cd ${HOME}

    # Create files needed
    check_file_exists_or_create "${SCRIPT_LOCATION}/Examples/moonraker.conf.example" "${PRINTER_DATA_CONFIG_PATH}/moonraker.conf" 
    check_file_exists_or_create "${SCRIPT_LOCATION}/Examples/printer.cfg.example" "${PRINTER_DATA_CONFIG_PATH}/printer.cfg" 
    check_file_exists_or_create "${SCRIPT_LOCATION}/Examples/vbrds-update-manager.conf.example" "${PRINTER_DATA_CONFIG_PATH}/vbrds-update-manager.conf" 

    # Patch klipper
    create_symbolic_link "${SCRIPT_LOCATION}/klipper/Extras/mesh_print_size.py" "${KLIPPER_PATH}/klippy/extras/mesh_print_size.py" 
    create_symbolic_link "${SCRIPT_LOCATION}/ExternalModules/ERCF/Klipper/ercf.py" "${KLIPPER_PATH}/klippy/extras/ercf.py" 
}

##################################################
# Step : Restart klipper
##################################################
restart_klipper()
{
    echo "Restarting Klipper..."
    sudo systemctl restart klipper
}

##################################################
# Step : Restart moonraker
##################################################
restart_moonraker()
{
    echo "Restarting moonraker..."
    sudo systemctl restart moonraker
}

####################################################################################################
# Run steps
####################################################################################################
# Parse command line arguments
while getopts "k:" arg; do
    case $arg in
        k) KLIPPER_PATH=$OPTARG;;
    esac
done

####################################################################################################

verify_ready
check_klipper
check_dependencies
restart_klipper
restart_moonraker

####################################################################################################
####################################################################################################