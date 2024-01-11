#!/usr/bin/python3
"""
Distributes archived pack to both web servers
"""

import os.path
from fabric.api import env, put, run

env.user = "ubuntu"
env.hosts = ["107.21.38.70", "100.26.213.217"]


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
