#!/usr/bin/python3
""" Function that deploys content of an archive """
import os
from datetime import datetime
from fabric.api import *
from fabric.operations import put
import shlex

env.hosts = ['100.26.244.129', '52.204.216.209']


def do_pack():
    """
    move contents of web_static to .tgz archive
    """
    dt = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    local('mkdir -p versions')
    test = local('tar -cvf versions/web_static_{}.tgz web_static'
                 .format(dt))
    if test.failed:
        return None
    else:
        return test


def do_deploy(archive_path):
    """ Search and deploy static archive to server """
    if not os.path.isfile(archive_path):
        print('archive file does not exist...')
        return False
    try:
        gzip = archive_path.split('/')[1]
        sans_gzip = gzip.split('.')[0]
    except Exception as e:
        print('Unable to get archive name')
        return False

    uploaded = put(archive_path, '/tmp/')
    if uploaded.failed:
        return False
    res = run('mkdir -p /data/web_static/releases/{}/'.format(sans_gzip))
    if res.failed:
        return False
    res = run('tar -C /data/web_static/releases/{} -xzf /tmp/{}'.format(
               sans_gzip, gzip))
    if res.failed:
        print('Archive opening unsuccessful')
        return False
    res = run('rm /tmp/{}'.format(gzip))
    if res.failed:
        print('Unable to delete archive...')
        return False
    res = run('mv /data/web_static/releases/{}/web_static/* \
               /data/web_static/releases/{}'
              .format(sans_gzip, sans_gzip))
    if res.failed:
        return False
    res = run('rm -rf /data/web_static/releases/{}/web_static'
              .format(sans_gzip))
    if res.failed:
        return False
    res = run('rm -rf /data/web_static/current')
    if res.failed:
        return False
    res = run('ln -sfn /data/web_static/releases/{} /data/web_static/current'
              .format(sans_gzip))
    if res.failed:
        return False
    print('\nNew Version Deployed!\n')

    return True
