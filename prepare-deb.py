#!/usr/bin/env python

# wget-debber.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

import sys
import requests
from bs4 import BeautifulSoup

import utils as u

urls = ['http://dev.kano.me/archive/pool/main/k/kano-toolset',
        'http://dev.kano.me/archive/pool/main/k/kano-profile']

if u.get_user() != 'root':
    sys.exit('Need to be root!')

for ur in urls:
    soup = BeautifulSoup(requests.get(ur).text)
    a = soup.find_all('a')[-1]['href']
    url = ur + '/' + a
    print url

    cmd = 'curl -L -v -o tmp.deb {url}'.format(url=url)
    _, e, _ = u.run_cmd(cmd)
    if '< HTTP/1.1 200 OK' in e:
        print 'download OK'
    else:
        print e
        sys.exit('Problem with download')

    cmd = 'gdebi tmp.deb -n -q -o APT::Install-Recommends=0 -o APT::Install-Suggests=0'
    o, e, rc = u.run_cmd(cmd)
    if rc == 0:
        print 'install OK'
    else:
        print o, e, rc
        sys.exit('Problem with gdebi')

u.deletefile('tmp.deb')





