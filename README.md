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

## Prepare system

If you are running `kano-debber` on your own system, you have to run the prepare script first. This is not needed on Kano-DevBox as it is already prepared.

	sudo ./prepare_system.sh
	
## How it works

`kano-debber` reads the list of repositories from the `repos` file, and the GitHub authentication token from `token`. The token file is optional and is only needed for private repositories.

The `repos` file has *repository - branch* definitions on each line, grouped by *sections* defined by `[section_name]` lines.

With each repository it can do three operations:

1. Download - it downloads the latest version from GitHub, using the token if specified 
2. Build - it builds the .deb package using the Debian `debuild` command
3. Install - it installs the previously built .deb package using the `gdebi` command

`kano-debber` processes each package in the order specified in the `repos` file. If you would like to have specific packages installed before others, move them higher up in the repos file.

## Usage

To use it, you need to specify what repost to download/build/install and 


 


download, build and install all packages

	sudo ./kano-debber.py -g all -dbi

with verbose output

	sudo ./kano-debber.py -g all -dbi -v


