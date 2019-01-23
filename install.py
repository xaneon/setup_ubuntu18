# !/usr/bin/python3
"""
This script needs to be run as root. 
sudo python3 install.py
"""

import os
import sys
import subprocess
from datetime import datetime

# TODO: set all parameters etc in a yaml or json file. Better in json because
# it is natively supported by python. yaml parsing requires an external module.
hostname = "ubuntu"
username = "bh"
gitusername = "Bonne Habekost"
gitemail = "bonne.habekost@gmail.com"
logfname = "install.log"
packagefile = "apt-packages"
python37version = "3.7.2"
linkfiles = "vim", "vimrc", "bashrc", "jupyter", "tmux.conf", "powerline"
mountdir = os.path.join(os.sep, "media", "sf_caumont")
dbdir = os.path.join(mountdir, "Dropbox")
dotdir = os.path.join(dbdir, "Dotfiles", "WHOTRSURFACE20")
homedir = os.path.join(os.sep, "home", username)
now = datetime.today().strftime("%Y%m%d_%M%H%S")

def log(func):
    def setlog(*args, **kwargs):
        r = func(*args, **kwargs)
        if r:
            with open(logfname, "a") as fid:
                fid.write(now + " --> " +
                          func.__name__ + ": " + decode(r))
        return r
    return setlog

@log
def run_cmd(cmd):
     output =  subprocess.Popen(cmd, shell=True,
                                stdout=subprocess.PIPE)
     content, status = output.communicate()

     if content:
        return content


def exists(fname):
    return os.path.exists(fname)


def make_fstruct():
    """ make folder structure with links. """
    for fname in linkfiles:
        curr_fname = homedir + os.sep + "." + fname
        dotfname = dotdir + os.sep + fname

        if exists(curr_fname):

            run_cmd("rm {}".format(curr_fname))
            run_cmd("ln -s {} {}".format(dotfname, curr_fname))
        else:
            run_cmd("ln -s {} {}".format(dotfname, curr_fname))


def decode(string):
    if string:
        return string.decode("utf-8")
    else:
        return ""

def getuser():
    username = run_cmd("echo $USER")
    if username:
        return decode(username).strip()
    else:
        return None

def getkernel():
    kernel = run_cmd("uname -r")
    if kernel:
        return decode(kernel).strip()
    else:
        return None

def sethostname(hostname):
    _ = run_cmd("hostname {}".format(hostname))

def read_packages(pfname):
    with open(pfname, "r") as fid:
        return [pack.strip() for pack in fid.readlines()]

def update():
    _ = run_cmd("apt-get update")

def check_package(packagename):
    return decode(run_cmd("dpkg -l {}".format(packagename)))

def check_and_install_packages():
    packages = read_packages(packagefile)
    update()
    for package in packages:
        curr_pcheck = check_package(package)
        if package in curr_pcheck:
            continue
        else:
            if "linux-headers" not in package:
                run_cmd("apt-get install {}".format(package))
            else:
                kernel = getkernel()
                run_cmd("apt-get install {}-{}".format(package, kernel))

def add_group(username, groupname):
    run_cmd("addgroup {} {}".format(username, groupname))

def install_python37(versionnumber):
    pyfname = "Python-{version}.tgz".format(version=versionnumber)
    if not exists(pyfname):
        run_cmd("wget " +
                "https://www.python.org/ftp/python/" +
                "{version}/{pyfname}".format(version=versionnumber, pyfname=pyfname))
        run_cmd("tar -xzvf {}".format(pyfname))
        os.chdir("Python-{version}".format(version=versionnumber))
        run_cmd("./configure --enable-optimizations")
        run_cmd("make")
        run_cmd("make install")
        run_cmd("rm {}".format(pyfname))
        run_cmd("rm -rf Python-{version}".format(version=versionnumber))

        # TODO: Not working properly because of permissions and output folder
        # etc.

def setgitconfig(gitusername, gitemail):
    run_cmd("git config --global user.email {}".format(gitemail))
    run_cmd("git config --global user.name {}".format(gitusername))

if __name__ == "__main__":
    # username = getuser()  # better user variable username 
                            # because the script might be run by root.
    sethostname(hostname)
    add_group(username, "vboxsf")
    # print(getkernel())
    make_fstruct()  # make the links and folderstructure
    check_and_install_packages()
    install_python37(python37version)
    setgitconfig(gitusername, gitemail)
    # TODO: Install virtualenv
