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

    if os.path.isfile(archive_path) is False:
        return False
    gzip = archive_path.split("/")[-1]
    capt = gzip.split(".")[0]

    if put(archive_path, "/tmp/{}".format(gzip)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(capt)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(capt)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(gzip, capt)).failed is True:
        return False
    if run("rm /tmp/{}".format(gzip)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(capt, capt)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(capt)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(capt)).failed is True:
        return False
    return True
