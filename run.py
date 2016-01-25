#!/usr/bin/env python

import sys
import time

_ENABLE_GUI = "--gui" in sys.argv

# If you don't want to see log messages on the console, uncomment the
# following line.  You might want to do this if you are using the GUI
# which displays logs itself.
# _DISABLE_CONSOLE_LOG = True


from hub import Hub as switch
# from the_router import DVRouter as switch

import cs176.core
import scenarios

time.sleep(1) # Wait a sec for log client to maybe connect

import scenarios.personalScenario as scenario
#import scenarios.candy as scenario
scenario.create()

# Import some stuff to use from the interpreter
import cs176.basics as basics
import cs176.api as api
import cs176.topo as topo

import logging
# There are two loggers: one that has output from the simulator, and one
# that has output from you (simlog and userlog respectively).  These are
# Python logger objects, and you can configure them as you see fit.  See
# http://docs.python.org/library/logging.html for info.
api.simlog.setLevel(logging.DEBUG)
api.userlog.setLevel(logging.DEBUG)

print """CS176A Network Simulator
You can get help on a lot of things.
For example, to see your current scenario, try help(scenario).
If you have a host named h1a, try help(h1a).
If you want to inspect a method of that host, try help(h1a.ping).
For help about the simulator and its API, try help(cs176) and help(api).
Type start() to start the simulator.
Good luck!"""

start = cs176.core.simulate
import code
code.interact(local=locals(), banner='')

