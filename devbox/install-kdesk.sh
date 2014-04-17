#!/usr/bin/env bash

# install kano-debber
./install-kano-debber.sh
cd kano-debber

# install compiled debs from repo
sudo ./prepare-deb.py

# download, build and install kdesk
sudo ./kano-debber.py -n kdesk -dbi

read -p "Install completed, press any key to continue..."


