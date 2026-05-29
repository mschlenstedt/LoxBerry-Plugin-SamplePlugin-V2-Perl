#!/usr/bin/perl

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
# LoxBerry::JSON->open() parses the JSON file and returns a hash reference.
# $lbpconfigdir is a LoxBerry system variable pointing to the plugin's
# config directory (/opt/loxberry/config/plugins/<folder>).
# https://wiki.loxberry.de/entwickler/perl_modules/loxberryjson
my $jsonobj = LoxBerry::JSON->new();
my $cfg = $jsonobj->open(filename => "$lbpconfigdir/pluginconfig.json", readonly => 1);

# Default form to "main" if not specified in the URL (?form=...)
$q->{form} = "main" if !$q->{form};

##########################################################################
# Form dispatch
##########################################################################

if ($q->{form} eq "main") {
	$template = LoxBerry::System::read_file("$lbptemplatedir/index.html");
	&form_main();
}
elsif ($q->{form} eq "logs") {
	$template = LoxBerry::System::read_file("$lbptemplatedir/logs.html");
	&form_logs();
}
else {
	$template = LoxBerry::System::read_file("$lbptemplatedir/index.html");
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

	# Übergabe des Config-Dateipfads an das Template.
	# Das JavaScript im Template nutzt diesen Pfad um beim Seitenaufruf
	# die gespeicherten Werte per AJAX zu laden (loadConfig) und beim
	# Klick auf Save zu schreiben (saveConfig).
	#
	# $lbpconfigdir endet mit dem Plugin-Ordnernamen, z.B.:
	#   /opt/loxberry/config/plugins/sampleplugin_folder
	# ajax-generic.php versteht den Platzhalter LBPCONFIG und expandiert
	# ihn zu $LBHOMEDIR/config/plugins.
	#
	# ajax-generic.php Doku:
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

	$navbar{10}{Name}   = "$L{'BASIC.LABEL_PERL_JQM'}";
	$navbar{10}{URL}    = 'index.cgi';
	$navbar{10}{active} = 1 if $q->{form} eq "main";

	$navbar{20}{Name}   = "$L{'BASIC.LABEL_PERL_NOJQM'}";
	$navbar{20}{URL}    = 'index_nojqm.cgi';

	$navbar{30}{Name}   = "$L{'BASIC.LABEL_PHP_JQM'}";
	$navbar{30}{URL}    = 'index_php.php';

	$navbar{40}{Name}   = "$L{'BASIC.LABEL_PHP_NOJQM'}";
	$navbar{40}{URL}    = 'index_php_nojqm.php';

	$navbar{90}{Name}   = "$L{'BASIC.LABEL_LOGS'}";
	$navbar{90}{URL}    = 'index.cgi?form=logs';
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
	# (e.g. errors written via LoxBerry::Log during daemon execution).
	# https://wiki.loxberry.de/entwickler/perl_modules/loxberrylog
	print LoxBerry::Log::get_notifications_html($lbpplugindir);

	print $templateout->output();

	# lbfooter() closes the jQuery Mobile page container and outputs
	# the LoxBerry page footer.
	# https://wiki.loxberry.de/entwickler/perl_modules/loxberryweb
	LoxBerry::Web::lbfooter();
	return();
}
