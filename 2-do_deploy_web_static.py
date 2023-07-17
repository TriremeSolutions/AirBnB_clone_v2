#!/usr/bin/python3
""" Function that deploys content of an archive """
from datetime import datetime
from fabric.api import *
import shlex
import os


env.hosts = ['100.26.244.129', '52.204.216.209']
env.user = "ubuntu"


def do_deploy(path_gzip):
    """ Search and deploy """
    if not os.path.exists(path_gzip):
        return False
    try:
        idd = path_gzip.replace('/', ' ')
        idd = shlex.split(idd)
        idd = idd[-1]

        xid = idd.replace('.', ' ')
        xid = shlex.split(xid)
        xid = xid[0]

        releases_path = "/data/web_static/releases/{}/".format(xid)
        tmp_path = "/tmp/{}".format(idd)

        put(path_gzip, "/tmp/")
        run("mkdir -p {}".format(releases_path))
        run("tar -xzf {} -C {}".format(tmp_path, releases_path))
        run("rm {}".format(tmp_path))
        run("mv {}web_static/* {}".format(releases_path, releases_path))
        run("rm -rf {}web_static".format(releases_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(releases_path))
        print("New version deployed!")
        return True
    except:
        return False
