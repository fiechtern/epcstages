# -*- coding: utf-8 -*-
import os
import sys

from fabric.api import cd, env, get, local, prefix, prompt, run
from fabric.utils import abort

env.hosts = ['stages.pierre-coullery.ch']

def clone_remote_db(dbtype='sqlite'):
    """
    Copy remote data (JSON dump), download it locally and recreate a local
    SQLite database with those data.
    """
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from common import settings

    db_path = settings.DATABASES['default']['NAME']
    if os.path.exists(db_path):
        rep = prompt('A local database (%s) already exists. Overwrite? (y/n)' % db_path)
        if rep == 'y':
            os.remove(db_path)
        else:
            abort("Database not copied")

    # Dump remote data and download the file
    with cd('/var/www/epcstages'):
        with prefix('source /var/venvs/stages/bin/activate'):
            run('python manage.py dumpdata --indent 1 contenttypes auth stages > epcstages.json')
        get('epcstages.json', '.')

    # Recreate a fresh DB with downloaded data
    local("python ../manage.py syncdb --noinput")
    local("python ../manage.py migrate")
    local("python ../manage.py flush --noinput")
    local("python ../manage.py loaddata epcstages.json")
