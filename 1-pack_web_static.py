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
    gzip = 'versions/web_static_{}.tgz'.format(dt.strftime(fmt))
    if os.path.isdir("versions") is False:
        if local("sudo mkdir -p versions").failed is True:
            return None
        if local("sudo tar -cvzf {} web_static".format(gzip)).failed is True:
            return None
        file_path = gzip
        return file_path
