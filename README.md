kano-debber
===========

Small tool for the creation of deb packages from Kano GitHub repos.

Only supported on Debian Wheezy systems and on Kano-DevBox

## Installation

Download and extract the latest version

	rm -rf ~/kano-debber
	mkdir -p ~/kano-debber
	cd ~/kano-debber
	curl -H "Authorization: token 06e849a65eaf62f48b1fc4eb6085a71cbbd1db89" -L -o tmp.tgz https://api.github.com/repos/KanoComputing/kano-debber/tarball/master
	tar --strip-components 1 --show-transformed-names -xzvf tmp.tgz
	rm tmp.tgz

## Usage

1\. If you are running `kano-debber` on your own system, you have to run the prepare script first. This is not needed on Kano-DevBox as it is already prepared.

	sudo ./prepare_system.sh
	
2\. 

download, build and install all packages

	sudo ./kano-debber.py -g all -dbi

with verbose output

	sudo ./kano-debber.py -g all -dbi -v


