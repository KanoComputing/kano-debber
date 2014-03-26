#!/usr/bin/env bash

gdebi *kano-toolset*.deb -n
gdebi *kano-connect*.deb -n
gdebi *kano-profile*.deb -n

ln -s /usr/lib/python2.7/dist-packages ~/
chmod -R 777 /usr/share/kano-profile
pip install randomavatar
