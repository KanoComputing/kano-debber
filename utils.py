#!/usr/bin/env python

# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

import subprocess
import os
import shutil


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


def uniqify_list(seq):
    # Order preserving
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]


def get_user():
    return os.environ['LOGNAME']
