#!/usr/bin/env bash

# install kano-debber
mkdir -p /home/user/kano-debber
cd /home/user/kano-debber
curl -H "Authorization: token 06e849a65eaf62f48b1fc4eb6085a71cbbd1db89" -L -o tmp.tgz https://api.github.com/repos/KanoComputing/kano-debber/tarball/master
tar --strip-components 1 --show-transformed-names -xzvf tmp.tgz
rm tmp.tgz

# install compiled debs from repo
sudo ./prepare-deb.py

# download, build and install make snake
sudo ./kano-debber.py -n snake -dbi


