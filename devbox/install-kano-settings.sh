#!/usr/bin/env bash

# install kano-debber
/home/user/install-kano-debber.sh
cd /home/user/kano-debber

# prepare system
sudo ./prepare-system.sh

# install compiled debs from repo
sudo ./prepare-deb.py

# download, build and install kano-settings
sudo ./kano-debber.py -g base -n kano-settings -dbi

sudo chown -R user:user /home/user

read -p "Install completed, press any key to continue..."


