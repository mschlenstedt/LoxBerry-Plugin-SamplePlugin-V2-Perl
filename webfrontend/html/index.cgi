#!/usr/bin/perl

# webfrontend/html/index.cgi - Public (unauthenticated) web frontend entry point.
#
# Files in webfrontend/html/ are accessible WITHOUT login authentication.
# Only place pages here that are safe to show to unauthenticated users, e.g.
# a status widget embedded in an external dashboard.
#
# For pages that require the user to be logged in to LoxBerry, use
# webfrontend/htmlauth/index.cgi instead.
#
# This script is installed to $LBPHTML/<folder>/index.cgi during installation.

use strict;
use warnings;

use LoxBerry::System;

print "Content-type: text/html\n\n";
print "Hello from the public (unauthenticated) Sample Plugin page!\n";
print "Plugin version: " . LoxBerry::System::pluginversion() . "\n";
