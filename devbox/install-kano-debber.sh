#!/usr/bin/env bash

# install kano-debber
mkdir -p /home/user/kano-debber && cd /home/user/kano-debber
wget -qO- https://api.github.com/repos/KanoComputing/kano-debber/tarball/master | tar --strip-components 1 -xz

sudo chown -R user:user /home/user
