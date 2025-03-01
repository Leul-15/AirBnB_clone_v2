#!/usr/bin/python3
"""
Distributes archived pack to both web servers
"""
import os.path
from fabric.api import env, put, run, local
from datetime import datetime

env.user = "ubuntu"
env.hosts = ["107.21.38.70", "100.26.213.217"]


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


def do_deploy(archive_path):
    """Distributes an archive to a web server
    """
    if os.path.isfile(archive_path) is False:
        return False
    filename = archive_path.split("/")[-1]
    folder = filename.split(".")[0]

    if put(archive_path, "/tmp/{}".format(filename)).failed is True:
        return False

    if run("rm -rf /data/web_static/releases/{}/".
           format(folder)).failed is True:
        return False

    if run("mkdir -p /data/web_static/releases/{}/".
           format(folder)).failed is True:
        return False

    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(filename, folder)).failed is True:
        return False

    if run("rm /tmp/{}".format(filename)).failed is True:
        return False

    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".
           format(folder, folder)).failed is True:
        return False

    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(folder)).failed is True:
        return False

    if run("rm -rf /data/web_static/current").failed is True:
        return False

    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(folder)).failed is True:
        return False

    print("New version deployed!")
    return True


def deploy():
    """Creates archive then distributes it to a web server
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
