#!/usr/bin/perl

# jQuery Mobile variant — kept for reference only.
# For new plugins use index.cgi (LoxBerry Design System) instead.

##########################################################################
# Modules
##########################################################################

use CGI;
use LoxBerry::System;  # System variables ($lbpconfigdir etc.) and helpers
                       # https://wiki.loxberry.de/entwickler/perl_modules/loxberrysystem
use LoxBerry::Web;     # lbheader(), lbfooter(), loglist_html()
                       # https://wiki.loxberry.de/entwickler/perl_modules/loxberryweb
use LoxBerry::JSON;    # Read/write JSON config files
                       # https://wiki.loxberry.de/entwickler/perl_modules/loxberryjson
use LoxBerry::Log;     # Logging and notification display
                       # https://wiki.loxberry.de/entwickler/perl_modules/loxberrylog
use warnings;
use strict;

##########################################################################
# Variables
##########################################################################

my $cgi = CGI->new;
my $q   = $cgi->Vars;

# pluginversion() reads the version from plugin.cfg
# https://wiki.loxberry.de/entwickler/perl_modules/loxberrysystem
my $version = LoxBerry::System::pluginversion();

my $template;
my $templateout;
my %L;

# Load plugin config (read-only — writing is done via ajax-generic.php)
# https://wiki.loxberry.de/entwickler/perl_modules/loxberryjson
my $jsonobj = LoxBerry::JSON->new();
my $cfg = $jsonobj->open(filename => "$lbpconfigdir/pluginconfig.json", readonly => 1);

# Default form to "main" if not specified in the URL (?form=...)
$q->{form} = "main" if !$q->{form};

##########################################################################
# Logging
##########################################################################

# LoxBerry::Log->new() creates a log object.
#   name:    logical name of this log, shown in the LoxBerry Log Manager
#   package: plugin folder — auto-detected from $lbpplugindir when omitted
#   addtime: 1 = prepend a timestamp to every log line
# Full docs: https://wiki.loxberry.de/entwickler/perl_modules/loxberrylog
my $log = LoxBerry::Log->new(
	name    => 'index_with_jqm',
	package => $lbpplugindir,
	addtime => 1,
);

# LOGSTART() registers the log session in the LoxBerry log database so it
# appears in the Log Manager. Must be called before the first log message.
# Without it, log files are written to disk but invisible in the Log Manager.
$log->LOGSTART("index_with_jqm.cgi called");

# LOGINF() uses the first-created log object automatically (the "main" object).
# Other log levels: LOGDEB (debug), LOGOK, LOGWARN, LOGERR, LOGCRIT
# Alternatively call the method on a specific object: $log->INF("message")
# https://wiki.loxberry.de/entwickler/perl_modules/loxberrylog
LOGINF("form: $q->{form}");

##########################################################################
# Form dispatch
##########################################################################

if ($q->{form} eq "main") {
	$template = LoxBerry::System::read_file("$lbptemplatedir/index_with_jqm.html");
	&form_main();
}
elsif ($q->{form} eq "logs") {
	$template = LoxBerry::System::read_file("$lbptemplatedir/logs.html");
	&form_logs();
}
else {
	$template = LoxBerry::System::read_file("$lbptemplatedir/index_with_jqm.html");
	&form_main();
}

&printtemplate();
exit;

##########################################################################
# Forms
##########################################################################

sub form_main
{
	&preparetemplate();

	# Pass the config file path to the template.
	# JavaScript uses this path to load saved values on page load (loadConfig)
	# and to write values on Save click (saveConfig) — both via ajax-generic.php.
	#
	# ajax-generic.php docs:
	#   https://wiki.loxberry.de/entwickler/web_ui_development_in_loxberry/web_forms_client_server_communication_ajaxgenericphp
	my ($plugin_folder) = $lbpconfigdir =~ m{/([^/]+)$};
	$templateout->param("AJAXCFGFILE", "LBPCONFIG/$plugin_folder/pluginconfig.json");

	return();
}

sub form_logs
{
	&preparetemplate();
	# loglist_html() renders the log file list as HTML
	# https://wiki.loxberry.de/entwickler/perl_modules/loxberryweb
	$templateout->param("LOGLIST", LoxBerry::Web::loglist_html());
	return();
}

##########################################################################
# Prepare template
##########################################################################

sub preparetemplate
{
	# HTML::Template reads the template file and creates a template object.
	# global_vars:       variables set in parent templates are visible in includes
	# loop_context_vars: provides __first__, __last__ etc. inside TMPL_LOOPs
	# die_on_bad_params: 0 means unknown template variables are silently ignored
	$templateout = HTML::Template->new_scalar_ref(
		\$template,
		global_vars       => 1,
		loop_context_vars => 1,
		die_on_bad_params => 0,
	);

	# readlanguage() loads translations from templates/lang/language_XX.ini
	# and sets them as template variables AND fills %L for use in Perl code.
	# https://wiki.loxberry.de/entwickler/perl_modules/loxberrysystem
	%L = LoxBerry::System::readlanguage($templateout, "language.ini");

	# Navbar entries — numeric keys control the display order.
	# LoxBerry::Web::lbheader() reads this %navbar hash and renders the tab bar.
	# https://wiki.loxberry.de/entwickler/perl_modules/loxberryweb
	our %navbar;

	$navbar{10}{Name}   = "$L{'BASIC.LABEL_PERL_NOJQM'}";
	$navbar{10}{URL}    = 'index.cgi';

	$navbar{20}{Name}   = "$L{'BASIC.LABEL_PERL_JQM'}";
	$navbar{20}{URL}    = 'index_with_jqm.cgi';
	$navbar{20}{active} = 1 if $q->{form} eq "main";

	$navbar{30}{Name}   = "$L{'BASIC.LABEL_PHP_NOJQM'}";
	$navbar{30}{URL}    = 'index.php';

	$navbar{40}{Name}   = "$L{'BASIC.LABEL_PHP_JQM'}";
	$navbar{40}{URL}    = 'index_with_jqm.php';

	$navbar{90}{Name}   = "$L{'BASIC.LABEL_LOGS'}";
	$navbar{90}{URL}    = 'index_with_jqm.cgi?form=logs';
	$navbar{90}{active} = 1 if $q->{form} eq "logs";

	return();
}

##########################################################################
# Print page
##########################################################################

sub printtemplate
{
	# lbheader() outputs the full LoxBerry page header including navbar,
	# jQuery Mobile, and the LoxBerry CSS/JS framework.
	# Parameters: page title, help wiki URL, local help file
	# https://wiki.loxberry.de/entwickler/perl_modules/loxberryweb
	LoxBerry::Web::lbheader($L{'BASIC.LABEL_PLUGINTITLE'} . " V$version", "https://wiki.loxberry.de", "help.html");

	# get_notifications_html() displays any pending plugin notifications
	# https://wiki.loxberry.de/entwickler/perl_modules/loxberrylog
	print LoxBerry::Log::get_notifications_html($lbpplugindir);

	print $templateout->output();

	# lbfooter() closes the jQuery Mobile page container and outputs
	# the LoxBerry page footer.
	# https://wiki.loxberry.de/entwickler/perl_modules/loxberryweb
	LoxBerry::Web::lbfooter();
	return();
}
