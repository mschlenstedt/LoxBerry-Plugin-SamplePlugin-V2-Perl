<?php

# Copyright 2024 Michael Schlenstedt, michael@loxberry.de
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This is the nojqm variant of index_php.php.
# jQuery Mobile is NOT loaded. The page uses the LoxBerry Design System
# (lb-* CSS classes) instead. Pass true as the 4th argument to lbheader().
# Use lb-* classes in your templates instead of jQuery Mobile data-role attributes.

##########################################################################
# Modules / Includes
##########################################################################

require_once "loxberry_system.php";
require_once "loxberry_web.php";
require_once "loxberry_log.php";

##########################################################################
# Variables
##########################################################################

$version = LBSystem::pluginversion();

// Read form parameter
$form = isset($_REQUEST['form']) ? $_REQUEST['form'] : 'main';

// Language phrases
$L = LBSystem::readlanguage("language.ini");

// Load plugin config
$cfg = LBSystem::lbfromjson("$lbpconfigdir/pluginconfig.json");

##########################################################################
# Navbar
##########################################################################

$navbar[10]['Name']   = $L['BASIC.LABEL_MAIN'];
$navbar[10]['URL']    = 'index_php_nojqm.php?form=main';
$navbar[10]['active'] = ($form === 'main');

$navbar[90]['Name']   = $L['BASIC.LABEL_LOGS'];
$navbar[90]['URL']    = 'index_php_nojqm.php?form=logs';
$navbar[90]['active'] = ($form === 'logs');

##########################################################################
# Header (nojqm mode: LoxBerry Design System, no jQuery Mobile)
##########################################################################

// true as 4th parameter: jQuery Mobile is not loaded,
// LoxBerry Design System (lb-* classes) is used instead.
LBWeb::lbheader($L['BASIC.LABEL_PLUGINTITLE'] . " V$version", "https://wiki.loxberry.de", "help.html", true);

##########################################################################
# Form dispatch
##########################################################################

if ($form === 'main') {
	form_main();
} elseif ($form === 'logs') {
	form_logs();
} else {
	form_main();
}

##########################################################################
# Footer
##########################################################################

LBWeb::lbfooter();
exit;

##########################################################################
# Form: Main settings
##########################################################################

function form_main()
{
	global $L, $cfg;
	include "$lbptemplatedir/index.html";
}

##########################################################################
# Form: Log viewer
##########################################################################

function form_logs()
{
	global $L;
	echo LBWeb::loglist_html();
}
