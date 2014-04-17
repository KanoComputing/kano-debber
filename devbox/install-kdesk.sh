#!/usr/bin/env bash

# install kano-debber
/home/user/install-kano-debber.sh
cd /home/user/kano-debber

# install compiled debs from repo
sudo ./prepare-deb.py

# download, build and install kdesk
sudo ./kano-debber.py -n kdesk -dbi

sudo chown -R user:user /home/user

read -p "Install completed, press any key to continue..."
sudo killall pcmanfm

