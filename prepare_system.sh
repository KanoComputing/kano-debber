#!/usr/bin/env bash

# prepare package building
apt-get -y install build-essential debhelper devscripts gdebi curl libwxbase2.8-dev libwxgtk2.8-dev wx2.8-headers python-dev python-pygame --no-install-recommends

# prepare python
apt-get -y purge python-setuptools python-virtualenv python-pip
wget -q --no-check-certificate https://raw.github.com/pypa/pip/master/contrib/get-pip.py -O get-pip.py
python get-pip.py
rm get-pip.py

# install python modules
pip install requests

groupadd kanousers
usermod -a -G kanousers root
usermod -a -G kanousers user

