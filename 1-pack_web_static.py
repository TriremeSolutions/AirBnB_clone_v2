#!/usr/bin/python3
""" FabScript that archives the contents of a folder """
from os import path
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Compresses web_static dir to a tar gzip archive.
    """
    dt = datetime.now()
    fmt = "%Y%m%d%H%M%S"
    gzip = "./versions/web_static_{}.tgz".format(dt.strftime(fmt))
    if not path.isdir("versions"):
        if local("mkdir versions").failed:
            return None
    if local("sudo tar -cvzf {} web_static".format(gzip)).succeeded:
        return gzip
    return None

