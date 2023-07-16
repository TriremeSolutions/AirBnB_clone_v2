#!/usr/bin/python3
""" FabScript that archives the contents of a folder """
import os
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Compresses web_static dir to a tar gzip archive.
    """
    try:
        if not os.path.exists("versions"):
            local('mkdir versions')
        dt = datetime.utcnow()
        fmt = "%Y%m%d%H%M%S"
        path_gzip = 'versions/web_static_{}.tgz'.format(dt.strftime(fmt))
        local('tar -cvzf {} web_static'.format(path_gzip))
        return path_gzip
    except:
        return None
