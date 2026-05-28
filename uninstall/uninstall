#!/bin/bash

# uninstall - Executed when the plugin is uninstalled via the LoxBerry Plugin Manager.
# Runs as user "ROOT".
# Use this to clean up anything that your plugin created outside of its own plugin
# directories (e.g. system service entries, entries in /etc, external symlinks).
# The plugin's own directories (config, data, html, cgi, templates, log, bin, sbin)
# are removed automatically by LoxBerry - you do not need to delete them here.
# Use with caution - remember that all target systems may differ.
#
# Exit codes:
#   0 = success, uninstallation continues
#   1 = warning, uninstallation continues but a warning is shown
#
# All variables from /etc/environment are available in this script.
#
# Arguments passed to this script:
#   $0 = path to this script
#   $1 = temporary folder used during uninstallation (short form)
#   $2 = plugin short name (NAME from plugin.cfg)
#   $3 = plugin installation folder (FOLDER from plugin.cfg)
#   $4 = plugin version (VERSION from plugin.cfg)
#
# Output tags for colorized uninstaller log:
#   <OK>      green  - operation successful
#   <INFO>    blue   - informational message
#   <WARNING> yellow - non-fatal warning
#   <ERROR>   red    - error
#   <FAIL>    red    - failure

COMMAND=$0      # Path to this script
PTEMPDIR=$1     # Temporary folder during uninstallation
PSHNAME=$2      # Plugin short name
PDIR=$3         # Plugin installation folder
PVERSION=$4     # Plugin version

# Build full plugin-specific paths from environment variables
PCGI=$LBPCGI/$PDIR
PHTML=$LBPHTML/$PDIR
PTEMPL=$LBPTEMPL/$PDIR
PDATA=$LBPDATA/$PDIR
PLOG=$LBPLOG/$PDIR
PCONFIG=$LBPCONFIG/$PDIR
PSBIN=$LBPSBIN/$PDIR
PBIN=$LBPBIN/$PDIR

echo "<INFO> Command is: $COMMAND"
echo "<INFO> Temporary folder is: $PTEMPDIR"
echo "<INFO> Plugin short name is: $PSHNAME"
echo "<INFO> Installation folder is: $PDIR"
echo "<INFO> Plugin version is: $PVERSION"
echo "<INFO> Plugin CGI folder is: $PCGI"
echo "<INFO> Plugin HTML folder is: $PHTML"
echo "<INFO> Plugin Template folder is: $PTEMPL"
echo "<INFO> Plugin Data folder is: $PDATA"
echo "<INFO> Plugin Log folder is: $PLOG"
echo "<INFO> Plugin Config folder is: $PCONFIG"
echo "<INFO> Plugin SBIN folder is: $PSBIN"
echo "<INFO> Plugin BIN folder is: $PBIN"

# Add cleanup tasks here for anything your plugin created outside its own directories.
# Example: remove a symlink created by the plugin
# if [ -L /etc/some-link ]; then
#   rm /etc/some-link
#   echo "<OK> Removed symlink /etc/some-link"
# fi

exit 0
