kano-debber
===========

Small tool for the creation of deb packages from Kano GitHub repos.

**Note**: you are only supposed to run this on Debian based systems and in Kano-Devbox

## Installation

Download and extract the latest version

	rm -rf ~/kano-debber
	mkdir -p ~/kano-debber
	cd ~/kano-debber
	curl -H "Authorization: token 06e849a65eaf62f48b1fc4eb6085a71cbbd1db89" -L -o tmp.tgz https://api.github.com/repos/KanoComputing/kano-debber/tarball/master
	tar --strip-components 1 --show-transformed-names -xzvf tmp.tgz
	rm tmp.tgz

## Prepare system

If you are running `kano-debber` on your own system, you have to run the prepare script first. This is not needed on Kano-Devbox as it is already prepared.

	sudo ./prepare-system.sh

## How it works

`kano-debber` reads the list of repositories from the `repos` file, and the GitHub authentication token from `token`. The token file is optional and is only needed for private repositories.

The `repos` file has *repository - branch* definitions on each line, grouped by *sections* defined by `[section_name]` lines.

With each repository it can do three operations:

1. Download - it downloads the latest version from GitHub, using the token if specified
2. Build - it builds the .deb package using the Debian `debuild` commander
3. Install - it installs the previously built .deb package using the `gdebi` command

`kano-debber` processes each package in the order of how they are in the `repos` file. If you would like to have specific packages installed before others (dependencies), place them higher in the repos file.

## Usage

To use it, you need to specify what repos to work on and what to do.

### Selecting repos

You can select repos in two ways

1. By group - where each group is a section in the repos file, or "all"
2. By name - where a repos name or branch can be branched

If you want to select by group, use the `-g` or `--group` switch.

**Example**: to select all packages in the "base" group, run the command:

	./kano-debber.py -g base

If you want to select by name, use the `-n` or `--name` switch. In name selection, it's enough to type a substring of the repo name or branch.

**Example**: to select package "kano-settings" and "make-snake", you can run:

	./kano-debber -n sett snake

You can check which packages are selected by running `kano-debber` without any action (see below).

### Setting actions

- To download repo, set `-d` or `--down`
- To build a repo, set `-b` or `--build`
- To install a repo, set `-i` or `--install`

You can combine these switches, for example to download, build and install a package, run `-dbi`.

If you don't specify any switch, `kano-debber` just lists the selected packages.

**Note**: installation requires build, so to install you have to use either `-bi` or `-dbi`. If you just want to install an already built .deb, use the `gdebi` command line program.

### Additional switches

#### List mode

Use `-l` or `--list` to list all packages in the repos file

#### Verbose output

Use `-v` or `--verbose` to show the detailed log for all the processes. It'll show the download log, the build log and the install log.

## Examples

**Example**: to download, build and install all repos

	sudo ./kano-debber.py -g all -dbi

**Example**: above, but with verbose output

	sudo ./kano-debber.py -g all -dbi -v

**Example**: build and install the already downloaded repo "make-snake" and show the log files

	sudo ./kano-debber.py -n snake -bi -v



## TODO

- remove token
