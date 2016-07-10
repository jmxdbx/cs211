"""
P4_Utility.py. CIS 211 Spring 2016 Project 4 Final. 2016-05-28.
Author: Joel Berry
Credits: Project spec, starter code by Anthony Hornof, 2016-04-08.

Basic Model-View-Controller fire-fighting simulation.
"""

# User defined exception for bad command lines.
class BadLineError(Exception):
    pass

# User defined exception to pass message to exception-handling code.
class BadMsgError(Exception):
    pass
