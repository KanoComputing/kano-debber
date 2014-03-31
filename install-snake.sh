#!/usr/bin/env bash

# install kano-toolset
curl -L -o kano-toolset.deb http://dev.kano.me/archive/pool/main/k/kano-toolset/kano-toolset_1.0-61.20140329_all.deb
sudo gdebi kano-toolset.deb -n
rm kano-toolset.deb

# install kano-profile
curl -L -o kano-profile.deb http://dev.kano.me/archive/pool/main/k/kano-profile/kano-profile_1.0-5.20140324_all.deb
sudo gdebi kano-profile.deb -n
rm kano-profile.deb

# install kano-debber
mkdir -p ~/kano-debber
cd ~/kano-debber
curl -H "Authorization: token 06e849a65eaf62f48b1fc4eb6085a71cbbd1db89" -L -o tmp.tgz https://api.github.com/repos/KanoComputing/kano-debber/tarball/master
tar --strip-components 1 --show-transformed-names -xzvf tmp.tgz
rm tmp.tgz

# download, build and install make snake
sudo ./kano-debber.py -n snake -dbi


