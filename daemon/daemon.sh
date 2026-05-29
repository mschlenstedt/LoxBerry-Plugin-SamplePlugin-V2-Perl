#!/bin/bash

# daemon - Init script executed at LoxBerry boot time.
#
# This file must be named exactly "daemon" in your plugin archive.
# During installation it will be renamed to the plugin's NAME (from plugin.cfg)
# and placed in the LoxBerry daemon directory ($LBHOMEDIR/system/daemons/plugins/).
# It is then executed automatically at every system boot by loxberryinit.sh.
#
# IMPORTANT: This script runs as user "root".
# IMPORTANT: Make sure this script exits cleanly and quickly!
#   Start long-running processes as background daemons (with & or via screen/tmux).
#   If this script blocks, the entire LoxBerry boot sequence will hang.
#
# You can use all variables from /etc/environment in this script.
# The plugin-specific paths (LBPCGI, LBPHTML, etc.) are available via
# $LBHOMEDIR and the plugin folder from /data/system/plugindatabase.dat.

# Read the plugin's actual installation folder from the plugin database.
# Do not hardcode the folder name - it may have a numeric suffix (01, 02, ...).
# PLUGINNAME is set by LoxBerry based on the NAME in plugin.cfg.
# PLUGINDIR is the actual installation folder of this plugin.

# Example: start a background daemon process
# PLUGINDIR=$(grep -A2 "NAME=$PLUGINNAME" /data/system/plugindatabase.dat | grep FOLDER | cut -d= -f2)
# if [ -n "$PLUGINDIR" ]; then
#     MYBINARY="$LBHOMEDIR/webfrontend/cgi/plugins/$PLUGINDIR/mydaemon.pl"
#     if [ -x "$MYBINARY" ]; then
#         "$MYBINARY" &
#         logger "LoxBerry plugin $PLUGINNAME: daemon started (PID $!)"
#     fi
# fi

# Log a message to the system log so we can verify the daemon script ran
if [ -x /usr/bin/logger ]; then
    /usr/bin/logger "LoxBerry Sample Plugin: daemon script executed at boot"
fi

exit 0
