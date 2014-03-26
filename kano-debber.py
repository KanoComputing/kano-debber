#!/usr/bin/env python

import os
import subprocess
import shutil
import sys
import argparse


def run_cmd(cmd):
    process = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()
    returncode = process.returncode
    return stdout, stderr, returncode


def run_print_output_error(cmd):
    o, e, rc = run_cmd(cmd)
    if o or e:
        print '\ncommand: {}'.format(cmd)
    if o:
        print 'output:\n{}'.format(o.strip())
    if e:
        print '\nerror:\n{}'.format(e.strip())
    return o, e, rc


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

    data = dict()
    for i, l in enumerate(lines):
        if not l:
            continue

        if l[0] == '[':
            section = l.translate(None, '[]')
        else:
            if l[0] == '#':
                continue

            parts = l.split()
            if len(parts) != 2:
                sys.exit('bad line in repos file:\n{}'.format(l))
            repo, branch = l.split()

            data.setdefault(section, list()).append((repo, branch))

    return data


data = parse_repos()

# argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--down', action='store_true', help='download packages')
parser.add_argument('-b', '--build', action='store_true', help='build packages')
parser.add_argument('-i', '--install', action='store_true', help='install packages')
parser.add_argument('-l', '--list', action='store_true', help='list packages')
parser.add_argument('-s', '--select', help='select given packages', nargs='+')
parser.add_argument('group', choices=['all'] + data.keys(), help='package groups', nargs='*')
args = parser.parse_args()

print args

sys.exit()

# checking packages are present
_, _, rc_curl = run_cmd('which curl')
_, _, rc_debuild = run_cmd('which debuild')
_, _, rc_gdebi = run_cmd('which gdebi')

if rc_curl or rc_debuild or rc_gdebi:
    sys.exit('Run prepare_system.sh first')

# start
root = os.getcwd()
token = read_file_contents('token')
repos_all = [r for r in read_file_contents_as_lines('repos') if r and r[0] != '#']
github = 'https://api.github.com/repos/KanoComputing/{}/tarball/{}'


if not 'all' in sys.argv:
    include = None
    for argv in sys.argv[1:]:
        if '-select=' in argv:
            include = argv.replace('-select=', '').split(',')

    exclude = None
    for argv in sys.argv[1:]:
        if '-exclude=' in argv:
            exclude = argv.replace('-exclude=', '').split(',')

    repos_selected = []
    if include:
        for repo in repos_all:
            for s in include:
                if s.lower() in repo.lower():
                    repos_selected.append(repo)

    if exclude:
        for repo in repos_selected:
            for u in exclude:
                if s.lower() in repo.lower():
                    repos_selected.remove(repo)

else:
    repos_selected = repos_all

for r in repos_selected:
    print r

for repo in repos_selected:
    repo, branch = repo.split()
    url = github.format(repo, branch)

    # dir_str = '{}'.format(branch)
    dir_str = '{}___{}'.format(repo, branch)
    dir_path = os.path.join(root, dir_str)

    if 'down' in sys.argv:
        print "\nDownloading {} ...".format(dir_str)

        deletedir(dir_path)
        ensuredir(dir_path)
        os.chdir(dir_path)

        cmd = 'curl -H "Authorization: token {}" -L -o tmp.tgz {}'.format(token, url)
        run_print_output_error(cmd)

        cmd = 'tar --strip-components 1 --show-transformed-names -xzvf tmp.tgz'
        run_cmd(cmd)

        deletefile('tmp.tgz')

    if 'build' in sys.argv:
        changelog_file = os.path.join(dir_path, 'debian/changelog')
        if not os.path.exists(changelog_file):
            continue

        print "\nBuilding {} ...".format(dir_str)
        if not os.path.exists(dir_path):
            sys.exit("run down first for {}".format(dir_str))

        os.chdir(dir_path)
        run_print_output_error('debuild -i -us -uc -b')


paths = os.listdir(root)
for p in paths:
    fullpath = os.path.join(root, p)
    ext = os.path.splitext(fullpath)[1][1:]
    if ext == 'build' or ext == 'changes':
        os.remove(fullpath)




