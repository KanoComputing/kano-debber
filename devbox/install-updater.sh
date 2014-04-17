#!/usr/bin/env bash

# install kano-debber
cd ~
./install-kano-debber.sh
cd kano-debber

# install compiled debs from repo
sudo ./prepare-deb.py

# download, build and install updater
sudo ./kano-debber.py -n updater -dbi

read -p "Install completed, press any key to continue..."


