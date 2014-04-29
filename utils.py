#!/usr/bin/env python

# kano.utils
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

import os
import subprocess
import sys
import signal
import shutil
import datetime
import getpass
import pwd
import json


def run_cmd(cmd):
    process = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               preexec_fn=restore_signals)

    stdout, stderr = process.communicate()
    returncode = process.returncode
    return stdout, stderr, returncode


def run_term_on_error(cmd):
    o, e, rc = run_cmd(cmd)
    if e:
        sys.exit('\nCommand:\n{}\n\nterminated with error:\n{}'.format(cmd, e.strip()))
    return o, e, rc


def run_print_output_error(cmd):
    o, e, rc = run_cmd(cmd)
    if o or e:
        print '\ncommand: {}'.format(cmd)
    if o:
        print 'output:\n{}'.format(o.strip())
    if e:
        print '\nerror:\n{}'.format(e.strip())
    return o, e, rc


def is_gui():
    return 'DISPLAY' in os.environ


def read_file_contents(path):
    if os.path.exists(path):
        with open(path) as infile:
            return infile.read().strip()


def write_file_contents(path, data):
    if os.path.exists(path):
        with open(path, 'w') as outfile:
            outfile.write(data)


def read_file_contents_as_lines(path):
    if os.path.exists(path):
        with open(path) as infile:
            content = infile.readlines()
            lines = [line.strip() for line in content]
            return lines


def delete_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)


def delete_file(file):
    if os.path.exists(file):
        os.remove(file)


def zenity_show_progress(msg):
    if is_gui():
        p = subprocess.Popen('yes | zenity --progress --text="{}" --pulsate --no-cancel --auto-close --title="kano-updater"'.format(msg),
                             shell=True, preexec_fn=restore_signals)
        return p.pid


def restore_signals():
        signals = ('SIGPIPE', 'SIGXFZ', 'SIGXFSZ')
        for sig in signals:
            if hasattr(signal, sig):
                signal.signal(getattr(signal, sig), signal.SIG_DFL)


def kill_child_processes(parent_pid):
    cmd = "ps -o pid --ppid {} --noheaders".format(parent_pid)
    o, _, _ = run_cmd(cmd)
    processes = [int(p) for p in o.splitlines()]
    for process in processes:
        os.kill(process, signal.SIGTERM)


def get_date_now():
    return datetime.datetime.utcnow().isoformat()


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_user_getpass():
    return getpass.getuser()


def get_user():
    return os.environ['LOGNAME']


def get_user_unsudoed():
    if 'SUDO_USER' in os.environ:
        return os.environ['SUDO_USER']
    else:
        return os.environ['LOGNAME']


def get_home():
    return os.path.expanduser('~')


def get_home_by_username(username):
    return pwd.getpwnam(username).pw_dir


def get_cpu_id():
    cpuinfo_file = '/proc/cpuinfo'
    lines = read_file_contents_as_lines(cpuinfo_file)
    if not lines:
        return

    for l in lines:
        parts = [p.strip() for p in l.split(':')]
        if parts[0] == 'Serial':
            return parts[1].upper()


def get_mac_address():
    cmd = '/sbin/ifconfig -a eth0 | grep HWaddr'
    o, _, _ = run_cmd(cmd)
    if len(o.split('HWaddr')) != 2:
        return
    mac_addr = o.split('HWaddr')[1].strip()
    mac_addr_str = mac_addr.upper()
    if len(mac_addr_str) == 17:
        return mac_addr_str


def read_json(filepath, silent=True):
    try:
        return json.loads(read_file_contents(filepath))
    except Exception:
        if not silent:
            raise


def write_json(filepath, data, prettyprint=False):
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile, indent=2, sort_keys=True)
    if prettyprint:
        _, _, rc = run_cmd('which underscore')
        if rc == 0:
            cmd = 'underscore print -i {filepath} -o {filepath}'.format(filepath=filepath)
            run_cmd(cmd)


def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def uniqify_list(seq):
    # Order preserving
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]


def download_url(url, file_path):
    import requests
    try:
        with open(file_path, 'wb') as handle:
            request = requests.get(url, stream=True)
            if not request.ok:
                return False, request.text
            for block in request.iter_content(1024):
                if not block:
                    break
                handle.write(block)
        return True, None
    except Exception as e:
        return False, str(e)


def get_ip_location():
    import requests
    try:
        r = requests.get('http://www.telize.com/geoip')
        if r.ok:
            return r.ok, None, r.json()
        else:
            return r.ok, r.text, None
    except Exception:
        return False, 'Connection error', None
