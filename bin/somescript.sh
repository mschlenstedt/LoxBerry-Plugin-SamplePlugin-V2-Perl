#!/bin/bash

# bin/somescript.sh - Example script for the plugin bin directory.
#
# Files in the bin/ directory are installed to $LBPBIN/<folder>/ during plugin
# installation. They are executable by the "loxberry" user (not root).
# Use this directory for helper scripts that your web frontend (CGI) or cron jobs
# need to call - scripts that do NOT require root privileges.
#
# For scripts that need root privileges, use the sbin/ directory instead and
# add appropriate entries to sudoers/sudoers so loxberry can call them via sudo.
#
# The path to your bin directory at runtime is: $LBPBIN/<actual-plugin-folder>/
# You can read the actual folder name from /data/system/plugindatabase.dat.
#
# This script runs as user "loxberry".

echo "Sample script in the bin directory, running as: $(whoami)"
