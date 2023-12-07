#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["54.172.178.214", "100.25.159.141"]


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, f"/tmp/{file}").failed is True:
        return False
    if run(f"rm -rf /data/web_static/releases/{name}/").failed is True:
        return False
    if run(f"mkdir -p /data/web_static/releases/{name}/").failed is True:
        return False
    if run(f"tar -xzf /tmp/{file} -C /data/web_static/releases/{name}/").failed is True:
        return False
    if run(f"rm /tmp/{file}").failed is True:
        return False
    if run(f"mv /data/web_static/releases/{name}/web_static/* "
           "/data/web_static/releases/{name}/").failed is True:
        return False
    if run(f"rm -rf /data/web_static/releases/{name}/web_static").failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{name}/ /data/web_static/current").failed is True:
        return False
    return True
