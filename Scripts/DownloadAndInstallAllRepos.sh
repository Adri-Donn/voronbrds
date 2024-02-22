#!/bin/bash
##################################################
verify_ready()
{
    if [ "$EUID" -eq 0 ]; then
        echo "This script must not run as root"
        exit -1
    fi
}

##################################################
# $1 : Directory name of the repository
# $2 : Repository url
check_repo_exist_or_install()
{
    if [ -d $1 ]
    then
        echo "Repository $2 exist"
    else
        echo "Cloning repository"
        git clone $2

        echo "Installing repository"

        if [ -f "./$1/install.sh" ]
        then
            sh "./$1/install.sh"
        else
            echo "No installer found"
        fi
    fi
}

####################################################################################################
verify_ready

cd ${HOME}

# Check and install mainsail-config if not present
check_repo_exist_or_install "mainsail-config" https://github.com/mainsail-crew/mainsail-config.git

# Check and install pgcode if not present
check_repo_exist_or_install "CanBoot" https://github.com/Arksine/CanBoot.git

# Check and install kiauh if not present
check_repo_exist_or_install "kiauh" https://github.com/th33xitus/kiauh.git

## Check and install klicky if not present
#check_repo_exist_or_install "Klicky-Probe" https://github.com/jlas1/Klicky-Probe.git

# Check and install pgcode if not present
check_repo_exist_or_install "pgcode" https://github.com/Kragrathea/pgcode.git

## Check and install auto-z if not present
#check_repo_exist_or_install "klipper_z_calibration" https://github.com/protoloft/klipper_z_calibration.git

# Check and install crowsnest if not present
check_repo_exist_or_install "crowsnest" https://github.com/mainsail-crew/crowsnest.git

# Check and install sonar if not present
check_repo_exist_or_install "sonar" https://github.com/mainsail-crew/sonar.git

# Check and install moonraker-timelapse if not present
check_repo_exist_or_install "moonraker-timelapse" https://github.com/mainsail-crew/moonraker-timelapse.git
