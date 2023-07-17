#!/usr/bin/python3
""" FabScript that archives the contents of a folder """
from os.path import isdir
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Compresses web_static dir to a tar gzip archive.
    """
    dt = datetime.utcnow()
    fmt = "%Y%-m%-d%-H%-M%-S"
    path_gzip = 'versions/web_static_{}.tgz'.format(dt.strftime(fmt))
    if isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(path_gzip)).failed is True:
        return None
    return
