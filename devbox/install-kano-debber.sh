#!/usr/bin/env bash

# install kano-debber
cd ~
mkdir -p ~/kano-debber && cd ~/kano-debber
wget -qO- https://api.github.com/repos/KanoComputing/kano-debber/tarball/master | tar --strip-components 1 -xz

