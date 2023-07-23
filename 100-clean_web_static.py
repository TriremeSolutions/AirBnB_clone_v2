#!/usr/bin/python3
""" Fabfile deletes outdated tgz """
from fabric.api import *
import os

env.hosts = ['100.26.244.129', '52.204.216.209']


def do_clean(number=0):
    """
    Deletes archives that are out-of-date

    number is the number of the archives, including the most recent, to keep

    If number is 0 or 1, keep only the most recent version of your archive.
    if number is 2, keep the most recent, and second most recent version
    if number is 3, keep the 3 most recent archives... etc.
    """

    number = int(number)

    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    remote = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(remote, number))
