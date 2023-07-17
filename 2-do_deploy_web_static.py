#!/usr/bin/python3
""" Function that deploys content of an archive """
import os
from datetime import datetime
from fabric.api import env
from fabric.api import put
from fabric.api import run
import shlex

env.hosts = ['100.26.244.129', '52.204.216.209']


def do_deploy(archive_path):
    """ Search and deploy archive to server """
    if not os.path.exists(archive_path):
        return False
    try:
        gzip = archive_path.replace('/', ' ')
        gzip = shlex.split(gzip)
        gzip = gzip[-1]
        xid = gzip.replace('.', ' ')
        xid = shlex.split(xid)
        xid = xid[0]

        releases_path = "/data/web_static/releases/{}/".format(xid)
        tmp_path = "/tmp/{}".format(gzip)

        put(archive_path, "/tmp/")
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
