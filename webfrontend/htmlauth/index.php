<?php

# Primary entry point. Uses the LoxBerry Design System (lb-* classes), not jQuery Mobile.
# Pass true as the 4th argument to lbheader() to suppress jQuery Mobile loading.
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
$cfg = json_decode(file_get_contents("$lbpconfigdir/pluginconfig.json"));

##########################################################################
# Navbar
##########################################################################

$navbar[10]['Name']   = $L['BASIC.LABEL_PERL_NOJQM'];
$navbar[10]['URL']    = 'index.cgi';

$navbar[20]['Name']   = $L['BASIC.LABEL_PERL_JQM'];
$navbar[20]['URL']    = 'index_with_jqm.cgi';

$navbar[30]['Name']   = $L['BASIC.LABEL_PHP_NOJQM'];
$navbar[30]['URL']    = 'index.php?form=main';
$navbar[30]['active'] = ($form === 'main');

$navbar[40]['Name']   = $L['BASIC.LABEL_PHP_JQM'];
$navbar[40]['URL']    = 'index_with_jqm.php';

$navbar[90]['Name']   = $L['BASIC.LABEL_LOGS'];
$navbar[90]['URL']    = 'index.php?form=logs';
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
	global $L, $cfg, $lbptemplatedir;
	include "$lbptemplatedir/index_php.html";
}

##########################################################################
# Form: Log viewer
##########################################################################

function form_logs()
{
	global $L;
	echo LBWeb::loglist_html();
}
