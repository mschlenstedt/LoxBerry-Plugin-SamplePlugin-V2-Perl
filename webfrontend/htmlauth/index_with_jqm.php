<?php

# jQuery Mobile variant — kept for reference only.
# For new plugins use index.php (LoxBerry Design System) instead.

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

// Load plugin config (read-only — writing is done via ajax-generic.php)
// Note: use $plugincfg, not $cfg — $cfg is reserved by loxberry_system.php for general.json
$plugincfg = json_decode(file_get_contents("$lbpconfigdir/pluginconfig.json"));

##########################################################################
# Navbar
##########################################################################

$navbar[10]['Name']   = $L['BASIC.LABEL_PERL_NOJQM'];
$navbar[10]['URL']    = 'index.cgi';

$navbar[20]['Name']   = $L['BASIC.LABEL_PERL_JQM'];
$navbar[20]['URL']    = 'index_with_jqm.cgi';

$navbar[30]['Name']   = $L['BASIC.LABEL_PHP_NOJQM'];
$navbar[30]['URL']    = 'index.php';

$navbar[40]['Name']   = $L['BASIC.LABEL_PHP_JQM'];
$navbar[40]['URL']    = 'index_with_jqm.php?form=main';
$navbar[40]['active'] = ($form === 'main');

$navbar[90]['Name']   = $L['BASIC.LABEL_LOGS'];
$navbar[90]['URL']    = 'index_with_jqm.php?form=logs';
$navbar[90]['active'] = ($form === 'logs');

##########################################################################
# Header (jQuery Mobile loaded — default)
##########################################################################

LBWeb::lbheader($L['BASIC.LABEL_PLUGINTITLE'] . " V$version", "https://wiki.loxberry.de", "help.html");

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
	global $L, $lbpconfigdir, $lbptemplatedir;

	// Config file path for ajax-generic.php (read/write from JavaScript)
	$plugin_folder = basename($lbpconfigdir);
	$ajaxCfgFile   = "LBPCONFIG/$plugin_folder/pluginconfig.json";

	include "$lbptemplatedir/index_php_jqm.html";
}

##########################################################################
# Form: Log viewer
##########################################################################

function form_logs()
{
	global $L;
	echo LBWeb::loglist_html();
}
