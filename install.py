# !/usr/bin/python3
"""
This script needs to be run as root. 
sudo python3 install.py
"""

import os
import sys
import subprocess
import json
from datetime import datetime

configfile = "config.json"

def load_config(configfile):
    with open(configfile) as fid:
        config = json.loads("".join(fid.readlines()))
    config["paths"]["homedir"] = [os.sep, "home",
                                  config["credentials"]["username"]]
    config["time"] = datetime.today().strftime("%Y%m%d_%M%H%S")
    return config

def log(func):
    def setlog(*args, **kwargs):
        r = func(*args, **kwargs)
        if r:
            with open(config["files"]["logfname"], "a") as fid:
                fid.write(config["time"] + " --> " +
                          func.__name__ + ": " + decode(r))
        return r
    return setlog

@log
def run_cmd(cmd):
     output =  subprocess.Popen(cmd, shell=True,
                                stdout=subprocess.PIPE,
                                # stderr=subprocess.STDOUT, 
                                executable='/bin/bash')
     content, status = output.communicate()

     if content:
        return content


def exists(fname):
    return os.path.exists(fname)


def make_fstruct(config):
    """ make folder structure with links. """
    for fname in config["files"]["linkfiles"]:
        curr_fname = (os.path.join(*config["paths"]["homedir"]) + 
                      os.sep + "." + fname)
        dotfname = os.path.join(*[os.sep] +
                                 config["paths"]["dotdir"]) + os.sep + fname

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

def check_and_install_packages(config):
    packages = read_packages(config["files"]["packagefile"])
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

def lsdirs(path):
    allfiles = os.listdir(path)
    alldirs = [item for item in allfiles
               if os.path.isdir(os.path.join(path, item))]
    return alldirs


def setup_virtualenvs(config):
    # run_cmd("mkvirtualenv {}")
    # TODO: run pip install with cache enabled to avoid reinstall
    rootdir = os.path.join(*config["paths"]["homedir"] +
                            config["paths"]["virtualenvdir"])
    existingvirtualenvs = lsdirs(rootdir)
    for virtenv, settings in config["environments"]["virtualenvs"].items():
        if virtenv in existingvirtualenvs:
            print("{} already exists".format(virtenv))
        else:
            source = "source /usr/share/virtualenvwrapper/virtualenvwrapper.sh"
            interpreterpath = os.path.join(*[os.sep] + settings["bin"])
            pipcachedir = os.path.join(*config["paths"]["homedir"] + [".cache", "pip"])
            arguments = "-p {}".format(interpreterpath)
            packages = " ".join(settings["libs"])
            run_cmd("{} && mkvirtualenv {} {}".format(source, arguments, virtenv))
            pipcmd = "pip install {}".format(packages)
            print(pipcmd)
            run_cmd("{} && workon {} && {}".format(source, virtenv, pipcmd))
            run_cmd("chown -R {} {}".format(config["credentials"]["username"],
                                            rootdir + os.sep + virtenv))
            run_cmd("chown -R {} {}".format(config["credentials"]["username"], 
                                            pipcachedir))


            # TODO: pass options for virtualenv including cache and interpreter

def setgitconfig(gitusername, gitemail):
    run_cmd("git config --global user.email {}".format(gitemail))
    run_cmd("git config --global user.name {}".format(gitusername))

if __name__ == "__main__":
    config = load_config(configfile)  # read config from JSON file
    # username = getuser()  # better user variable username 
                            # because the script might be run by root.
    sethostname(config["credentials"]["hostname"])
    add_group(config["credentials"]["username"], "vboxsf")
    # print(getkernel())
    make_fstruct(config)  # make the links and folderstructure
    check_and_install_packages(config)
    install_python37(config["versions"]["python3.7"])
    setgitconfig(config["credentials"]["gitusername"], 
                 config["credentials"]["gitemail"])
    # TODO: Install virtualenv
    setup_virtualenvs(config)
