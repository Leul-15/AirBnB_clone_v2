#!/usr/bin/python3
"""
generates a .tgz archive from the contents of the web_static folder
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Fabric script that generates a .tgz archive from the
    contents of the web_static folder
    """
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filePath = 'versions/web_static_{}.tgz'.format(timestamp)

    local('mkdir -p versions/')
    newArchive = local('tar -cvzf {} web_static/'.format(filePath))

    if newArchive.succeeded:
        return filePath
