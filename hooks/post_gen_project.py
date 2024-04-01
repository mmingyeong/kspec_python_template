# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.

import os
import shutil

import invoke
from invoke.exceptions import UnexpectedExit

#
# This script runs after the cookiecutter template has been installed
#

PACKAGING_SYSTEM = '{{ cookiecutter.packaging_system }}'

GITUSER = '{{ cookiecutter.github_organisation }}'
PKGNAME = '{{ cookiecutter.package_name }}'

CURRENTDIR = os.path.abspath(os.curdir)
PYTHONDIR = os.path.join(CURRENTDIR, 'python')


def copy_packaging_system():
    """Copies the appropriate files to use setup.cfg or poetry."""

    # Initially the repo is created with two directories, setup_cfg and poetry
    # that contain the files needed for each packaging system. Here, depending
    # on the cookiecutter configuration, we move the appropriate files and
    # remove the other ones.

    pack_dir = 'poetry'

    files = os.listdir(pack_dir)
    for file_ in files:
        if file_ == '__main__.py':
            shutil.move(os.path.join(pack_dir, file_), os.path.join(PYTHONDIR, PKGNAME))
        else:
            shutil.move(os.path.join(pack_dir, file_), CURRENTDIR)

    # Delete both directories
    for dir_ in ['poetry']:
        shutil.rmtree(dir_, ignore_errors=True)


@invoke.task
def install(ctx):
    ''' Cleans and installs the new repo '''

    os.chdir(CURRENTDIR)
    print('Installing {0}'.format(PKGNAME))
    ctx.run("python setup.py clean")
    try:
        ctx.run("python -d setup.py install", hide='both')
    except UnexpectedExit as e:
        print('Unexpected failure during install:\n {0}'.format(e.result.stderr))
        permden = '[Errno 13] Permission denied' in e.result.stderr
        if permden:
            print('Permission denied during install.  Trying again with sudo')
            ctx.run('sudo python -d setup.py install')

col = invoke.Collection(install)
ex = invoke.executor.Executor(col)

print('Please add {0} into your PYTHONPATH!'.format(PYTHONDIR))