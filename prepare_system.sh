#!/usr/bin/env bash

# prepare package building
sudo apt-get -y --no-install-recommends install build-essential curl debhelper devscripts fping gdebi libwxbase2.8-dev libwxgtk2.8-dev python python-dev python-gtk2 python-pygame python-webkit rxvt-unicode-256color udhcpc wx2.8-headers

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

