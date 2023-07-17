#!/usr/bin/python3
""" FabScript that archives the contents of a folder """
import os.path
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Compresses web_static dir to a tar gzip archive.
    """
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file
