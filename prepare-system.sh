#!/usr/bin/env bash

# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

# prepare package building
sudo apt-get -y --no-install-recommends install build-essential curl \
    debhelper devscripts fakeroot fping gdebi libwxbase2.8-dev libwxgtk2.8-dev openjdk-7-jre \
    python python-dev python-gtk2 python-pygame python-webkit rxvt-unicode-256color \
    udhcpc wx2.8-headers zenity  libx11-dev libxft-dev libimlib2-dev \
    libstartup-notification0-dev libao-dev libmpg123-dev libxss-dev git

# prepare python
sudo apt-get -y purge python-setuptools python-virtualenv python-pip
wget -q --no-check-certificate https://raw.github.com/pypa/pip/master/contrib/get-pip.py -O get-pip.py
python get-pip.py
rm get-pip.py

# install python modules
sudo pip install --upgrade requests beautifulsoup4 pam python-slugify

