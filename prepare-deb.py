#!/usr/bin/env python

# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

import sys
import requests
from utils import get_user, run_cmd, delete_file

packages_needed = ['kano-toolset', 'kano-profile']
packages_file_url = 'http://80.243.184.98/archive/dists/devel/main/binary-armhf/Packages'

if get_user() != 'root':
    sys.exit('Need to be root!')

error = None
try:
    r = requests.get(packages_file_url)
    if r.ok:
        packages_file_str = r.text
    else:
        error = r.text
except Exception:
    error = 'Connection error'

if error:
    sys.exit('Problem with downloading packages files: {}'.format(error))

for p in packages_needed:
    download_file = False
    for line in packages_file_str.splitlines():
        if line == 'Package: {}'.format(p):
            download_file = True
        if line.startswith('Filename: ') and download_file:
            download_url = line.split('Filename: ')[1]
            full_download_url = 'http://80.243.184.98/archive/' + download_url
            download_file = False

            print 'Downloading {} {}'.format(p, download_url)

            cmd = 'curl -L -v -o tmp.deb {url}'.format(url=full_download_url)
            _, e, _ = run_cmd(cmd)
            if '< HTTP/1.1 200 OK' in e:
                print 'download OK'
            else:
                print e
                sys.exit('Problem with download')

            cmd = 'gdebi tmp.deb -n -q -o APT::Install-Recommends=0 -o APT::Install-Suggests=0'
            o, e, rc = run_cmd(cmd)
            if rc == 0:
                print 'install OK'
            else:
                print o, e, rc
                sys.exit('Problem with gdebi')

            print

delete_file('tmp.deb')





