#!/usr/bin/python3
""" FabScript that archives the contents of a folder """
import os.path
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Compresses web_static dir to a tar gzip archive.
    """
    dt = datetime.now()
    fmt = "%Y%m%d%H%M%S"
    path_gzip = "./versions/web_static_{}.tgz".format(dt.strftime(fmt))
    if os.path.isdir("versions") is False:
        if local("mkdir versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(path_gzip)).failed is True:
        return None
    return path_gzip
