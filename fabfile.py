#!/usr/bin/env python
# -*- coding: utf-8 -*-

GIT_ORIGIN = ''

__version__ = (1, 0, 0, 'final')

import sys
import os
import datetime
import time
from fabric.api import *


BASE_HEADER = """%(now)s
using project '%(app)s'
%(desc)s

"""

##
## available commands
##

def provision(update_rep=False):
    # starts provision
    start = time.time()

    # validate environment
    if not hasattr(env, 'app_root'):
        print 'ERROR: unknown environment.'
        os.sys.exit(1)

    sys.stdout.write(BASE_HEADER % {
        "now": datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"),
        "app": env.app, "desc": "Provision local developer enviroment"
    })

    with lcd(env.path):
        # Create virtualenv if not exists
        if not os.path.exists(env.virtual):
            command = "virtualenv %s" % env.virtual
            local(command)

        # allow to update repository
        if getattr(env, 'git_branch', None):
            # clone repository
            command = 'test -d %s/.git || git clone %s %s -b %s'
            local(command % (env.app_root, env.git_origin, env.app_root, env.git_branch))

            # update repository
            command = 'git checkout %s && git pull origin %s'
            local(command % (env.git_branch, env.git_branch))

        # Run install in requirements
        command = "%(pip)s install -r %(requirements_file)s" % env
        local(command)

        # Run database migrations
        command = "%(python)s %(manage_file)s migrate" % env
        local(command)

    final = time.time()
    puts('\nexecution finished in %.2fs' % (final - start))


##
## available environments
##
def localhost():
    env.app = 'example'
    env.app_root = os.path.join(os.path.dirname(__file__), 'example')
    env.git_origin = GIT_ORIGIN
    env.manage_file = os.path.join(os.path.dirname(__file__), 'manage.py')
    env.requirements_file = 'requirements.txt'
    env.virtual = os.path.join(os.path.dirname(__file__), '.virtualenv')
    env.pip = os.path.join(env.virtual, "bin", "pip")
    env.python = os.path.join(env.virtual, "bin", "python")