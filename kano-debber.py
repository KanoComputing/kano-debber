#!/usr/bin/env python

import os
import subprocess
import shutil
import sys
import argparse
from collections import OrderedDict


def run_cmd(cmd):
    process = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()
    returncode = process.returncode
    return stdout, stderr, returncode


def read_file_contents(path):
    if os.path.exists(path):
        with open(path) as infile:
            return infile.read().strip()


def read_file_contents_as_lines(path):
    if os.path.exists(path):
        with open(path) as infile:
            content = infile.readlines()
            lines = [line.strip() for line in content]
            return lines


def ensuredir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def deletefile(file):
    if os.path.exists(file):
        os.remove(file)


def deletedir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)


def parse_repos():
    lines = read_file_contents_as_lines('repos')
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


def uniqify_list(seq):
    # Order preserving
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]


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
repos_selected = uniqify_list(repos_selected)

print 'Selected repos:'
for r in repos_selected:
    print r[0], r[1]


# checking packages are present
_, _, rc_curl = run_cmd('which curl')
_, _, rc_debuild = run_cmd('which debuild')
_, _, rc_gdebi = run_cmd('which gdebi')

if rc_curl or rc_debuild or rc_gdebi:
    sys.exit('Run prepare_system.sh first')

# start
root_dir = os.getcwd()
token = read_file_contents('token')
github = 'https://api.github.com/repos/KanoComputing/{}/tarball/{}'


for name, branch in repos_selected:
    url = github.format(name, branch)
    dir_str = '{}___{}'.format(name, branch)
    dir_path = os.path.join(root_dir, dir_str)
    debfile = ''

    if args.down:
        print '\nDownloading {} ...'.format(dir_str)

        deletedir(dir_path)
        ensuredir(dir_path)
        os.chdir(dir_path)

        if not token:
            cmd = 'curl -L -v -o tmp.tgz {url}'.format(url=url)
        else:
            cmd = 'curl -H "Authorization: token {token}" -L -v -o tmp.tgz {url}'.format(token=token, url=url)
        _, e, _ = run_cmd(cmd)

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
        run_cmd(cmd)

        deletefile('tmp.tgz')

    if args.build:
        print '\nBuilding {} ...'.format(dir_str)
        if not os.path.exists(dir_path) or not os.listdir(dir_path):
            sys.exit('You need to download first!')

        changelog_file = os.path.join(dir_path, 'debian/changelog')
        if not os.path.exists(changelog_file):
            print 'No changelog, skipped!'
            continue

        os.chdir(dir_path)
        cmd = 'debuild -i -us -uc -b'
        o, e, rc = run_cmd(cmd)
        if args.verbose:
            print o
        if rc == 0:
            print 'OK'
        else:
            print e
            sys.exit('Problem with building!')

        debline = [l for l in o.splitlines() if 'dpkg-deb: building package' in l][0]
        debfile = debline.split('in `../')[1][:-2]
        debfile_path = os.path.join(root_dir, debfile)
        if not os.path.exists(debfile_path):
            sys.exit('Problem with parsing build log, .deb file: {}'.format(debfile))

        # cleanup .build and .changes
        [os.remove(os.path.join(root_dir, f))
         for f in os.listdir(root_dir)
         if os.path.splitext(f)[1][1:] in ['build', 'changes']]

    if args.install:
        os.chdir(root_dir)
        print '\nInstalling {} ...'.format(dir_str)

        if not debfile:
            msg = 'You need to build before install!\n'
            msg += 'To manually install an already built package, please use `gdebi packagename`'
            sys.exit(msg)

        print 'using .deb file: {}'.format(debfile)

        cmd = 'gdebi {} -n -q'.format(debfile_path)
        o, e, rc = run_cmd(cmd)
        if args.verbose:
            print o
        if rc == 0:
            print 'OK'
        else:
            print e
            sys.exit('Problem with installing!')








