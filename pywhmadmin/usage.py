#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import textwrap

description="\tMore Details: -v|--verbose for detailed description"

verbose_description=textwrap.dedent('''\
A python wrapper for WHM and cPanel.
------------------------------------
This utility provides access to the various APIs
available in WHM and cPanel.

Remote administration is possible by specifying
a host, username, and password.  In most cases
root privileges will be required.  If no password
is provided in the command, the user will be
prompted.

The exception is execution on localhost, which
will instead call the cPanel/WHM api scripts as
root unless another user is provided.

Detailed Usage
------------------------------------
python pywhmadmin.py [OPTION]... [API] [FUNC] [PARAMS]...
python pywhmadmin.py [OPTION]... [SCRIPT_NAME] [PARAMS]...
python pywhmadmin.py [OPTION]... [CMD] [PARAMS]...

It is recommended to create an alias under your administrative
user's .bashrc or some include therein and be sure pywhmadmin.py
is on the system PATH:
alias pywhm="python2.7 pywhmadmin.py"

In each case, the PARAMS list will be literally passed
to the script or API function specified.

An exception to this would be any CMD passed from the
following list, which expect specific paramters and
do more than simple API or script calls.  These commands
will print reports to stdout by default:

CMD             PARAMS          DESCRIPTION
-------------------------------------------------------------
domlist         user(s)*        Displays a user domain report
acctinfo        user(s)*        Displays a user account summary

* Omitting the user parameter will run the given command
on the root user.

In general, parameter lists should be comma-separated
WITHOUT spaces - user1,user2,user3 - or quoted if
spaces must be present.

Examples
------------------------------------
pywhmadmin whm1 resetzone domain="example.com"
pywhmadmin domlist user > user_domlist.txt
pywhmadmin --host server.example.com listaccts
''')

epilog='\tGuide: https://pokeybill.us/pywhmadmin\n'

verbose_epilog=textwrap.dedent('''\
Additional Resources
------------------------------------
cPanel API v1:  https://confluence2.cpanel.net/display/SDK/Guide+to+cPanel+API+1
cPanel API v2:  https://documentation.cpanel.net/display/SDK/Guide+to+cPanel+API+2
WHM API v1:     https://documentation.cpanel.net/display/SDK/Guide+to+WHM+API+1

Guide:          https://pokeybill.us/pywhmadmin
''')

