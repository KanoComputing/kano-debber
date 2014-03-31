#!/usr/bin/env python

# kano-debber.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

import os
import sys
import argparse
from collections import OrderedDict

import utils as u


def parse_repos():
    lines = u.read_file_contents_as_lines('repos')
    if not lines:
        sys.exit('error with repos file')

    data = OrderedDict()
    section = ''
    for i, l in enumerate(lines):
        if not l:
            continue

        if l[0] == '[':
            section = l.translate(None, '[]')
        else:
            if l[0] == '#':
                continue

            if not section:
                sys.exit('Error with repos file, needs to start with a section!')

            parts = l.split()
            if len(parts) != 2:
                sys.exit('Bad line in repos file:\n{}'.format(l))
            repo, branch = l.split()

            data.setdefault(section, list()).append((repo, branch))
    return data


# parse repos
repos_list = parse_repos()

# argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--down', action='store_true', help='download packages')
parser.add_argument('-b', '--build', action='store_true', help='build packages')
parser.add_argument('-i', '--install', action='store_true', help='install packages')
parser.add_argument('-l', '--list', action='store_true', help='list packages')
parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
parser.add_argument('-n', '--name', help='select by name', nargs='+')
parser.add_argument('-g', '--group', choices=['all'] + repos_list.keys(), help='select by group', nargs='+')
args = parser.parse_args()


if args.list:
    print 'List of repos:'
    for group, repos in repos_list.iteritems():
        print group
        for r in repos:
            print r[0], r[1]
        print
    sys.exit()

repos_selected = []

# group selection
if args.group:
    if 'all' in args.group:
        repos_selected = sum(repos_list.values(), [])
    else:
        for g in args.group:
            for r in repos_list[g]:
                repos_selected.append(r)

# name selection
if args.name:
    for n in args.name:
        for r in sum(repos_list.values(), []):
            if n.lower() in r[0].lower() or n.lower() in r[1].lower():
                repos_selected.append(r)

if not repos_selected:
    sys.exit('No repo selected, run -h for help')

# uniqify repos_selected
repos_selected = u.uniqify_list(repos_selected)

print 'Selected repos:'
for r in repos_selected:
    print r[0], r[1]

if not (args.down or args.build or args.install):
    sys.exit()


# checking packages are present
_, _, rc_curl = u.run_cmd('which curl')
_, _, rc_debuild = u.run_cmd('which debuild')
_, _, rc_gdebi = u.run_cmd('which gdebi')

if rc_curl or rc_debuild or rc_gdebi:
    sys.exit('Run prepare_system.sh first')

# start
root_dir = os.getcwd()
token = u.read_file_contents('token')
github = 'https://api.github.com/repos/KanoComputing/{}/tarball/{}'


for name, branch in repos_selected:
    url = github.format(name, branch)
    dir_str = '{}___{}'.format(name, branch)
    dir_path = os.path.join(root_dir, dir_str)
    debfile = ''
    print

    if args.down:
        print 'Downloading {} ...'.format(dir_str)

        u.deletedir(dir_path)
        u.ensuredir(dir_path)
        os.chdir(dir_path)

        if not token:
            cmd = 'curl -L -v -o tmp.tgz {url}'.format(url=url)
        else:
            cmd = 'curl -H "Authorization: token {token}" -L -v -o tmp.tgz {url}'.format(token=token, url=url)
        _, e, _ = u.run_cmd(cmd)

        if args.verbose:
            print e

        if '< Status: 302 Found' in e:
            print 'OK'
        else:
            msg = 'Problem with download, possibly missing token?'
            if not args.verbose:
                msg += ' Use -v for detailed error'
            sys.exit(msg)

        cmd = 'tar --strip-components 1 --show-transformed-names -xzvf tmp.tgz'
        u.run_cmd(cmd)

        u.deletefile('tmp.tgz')

    if args.build:
        print 'Building {} ...'.format(dir_str)

        # checking path
        if not os.path.exists(dir_path) or not os.listdir(dir_path):
            sys.exit('You need to download first!')

        # checking changelog file
        changelog_file = os.path.join(dir_path, 'debian/changelog')
        if not os.path.exists(changelog_file):
            print 'No changelog, build skipped'
            continue

        # checking root
        if u.get_user() != 'root':
            sys.exit('Need to be root to build packages!')

        os.chdir(dir_path)
        cmd = 'debuild -i -us -uc -b'
        o, e, rc = u.run_cmd(cmd)
        if args.verbose:
            print o
        if rc == 0:
            print 'OK'
        else:
            print e
            sys.exit('Problem with building!')

        deblines = [l for l in o.splitlines() if 'dpkg-deb: building package' in l]
        debfiles = []
        for debline in deblines:
            debfile = debline.split('in `../')[1][:-2]
            debfile_path = os.path.join(root_dir, debfile)
            if not os.path.exists(debfile_path):
                sys.exit('Problem with parsing build log, .deb file: {}'.format(debfile))
            else:
                debfiles.append((debfile, debfile_path))

        # cleanup .build and .changes
        [os.remove(os.path.join(root_dir, f))
         for f in os.listdir(root_dir)
         if os.path.splitext(f)[1][1:] in ['build', 'changes']]

    if args.install:
        print 'Installing {} ...'.format(dir_str)
        if u.get_user() != 'root':
            sys.exit('Need to be root to install packages!')

        success = True
        for debfile, debfile_path in debfiles:
            if not debfile:
                msg = 'You need to build before install!\n'
                msg += 'To manually install an already built package, please use `gdebi packagename`'
                sys.exit(msg)

            if args.verbose:
                print 'using .deb file: {}'.format(debfile)

            cmd = 'gdebi {} -n -q'.format(debfile_path)
            o, e, rc = u.run_cmd(cmd)
            if args.verbose:
                print o

            success = success and rc == 0

            # detect newly installed dependencies
            str = 'Setting up '
            deps = [l[len(str):].replace(' ...', '')
                    for l in o.splitlines()
                    if l.startswith(str)]
            if deps:
                print 'Newly installed packages: {}'.format(' '.join(deps))

        if success:
            print 'OK'
        else:
            print e
            sys.exit('Problem with installing!')
