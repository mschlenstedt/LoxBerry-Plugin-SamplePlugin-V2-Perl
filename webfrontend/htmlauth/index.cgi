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

	# ------------------------------------------------------------------
	# Pass config values to the template so every form field is
	# pre-filled with the saved value when the page loads.
	#
	# How it works:
	#   1. We read $cfg (loaded above) — it contains the JSON content
	#      of pluginconfig.json as a Perl hash reference.
	#   2. We call $templateout->param("VARNAME", value) to set a
	#      template variable.  In the HTML template, <TMPL_VAR VARNAME>
	#      is replaced by that value.
	#   3. For checkboxes/radio buttons we pass 1 (true) or 0 (false).
	#      <TMPL_IF VARNAME>checked="checked"</TMPL_IF> then adds the
	#      HTML attribute only when the value is true.
	#
	# HTML::Template variable system:
	#   https://wiki.loxberry.de/entwickler/plugin_fur_den_loxberry_entwickeln_ab_version_1x/html-template_variable_system
	# ------------------------------------------------------------------

	# Build the ajax-generic.php file path for JavaScript.
	# $lbpconfigdir ends with the plugin folder name, e.g.
	#   /opt/loxberry/config/plugins/sampleplugin_folder
	# ajax-generic.php understands the placeholder LBPCONFIG which it
	# expands to $LBHOMEDIR/config/plugins — so
	#   LBPCONFIG/sampleplugin_folder/pluginconfig.json
	# is the same file as $lbpconfigdir/pluginconfig.json.
	# ajax-generic.php docs:
	#   https://wiki.loxberry.de/entwickler/web_ui_development_in_loxberry/web_forms_client_server_communication_ajaxgenericphp
	my ($plugin_folder) = $lbpconfigdir =~ m{/([^/]+)$};
	$templateout->param("AJAXCFGFILE", "LBPCONFIG/$plugin_folder/pluginconfig.json");

	# --- Text and numeric fields: pass value as string ----------------

	$templateout->param("CFG_TEXT1",     $cfg->{MAIN}{text1}       // "");
	$templateout->param("CFG_DATE1",     $cfg->{MAIN}{date1}       // "");
	$templateout->param("CFG_RANGE_MIN", $cfg->{MAIN}{'range-min'} // "20");
	$templateout->param("CFG_RANGE_MAX", $cfg->{MAIN}{'range-max'} // "80");
	$templateout->param("CFG_SLIDER1",   $cfg->{MAIN}{slider1}     // "50");

	# --- Boolean fields: pass 1 (true) or 0 (false) -------------------
	# The template uses <TMPL_IF CFG_...>checked="checked"</TMPL_IF>
	# HTML::Template treats 0 as false and 1 as true, same as Perl.

	$templateout->param("CFG_CHECKBOX1", ($cfg->{MAIN}{checkbox1} // "0") eq "1" ? 1 : 0);
	$templateout->param("CFG_FLIP1",     ($cfg->{MAIN}{flip1}     // "0") eq "1" ? 1 : 0);

	# --- Radio button groups: exactly one option is true --------------

	my $rv = $cfg->{MAIN}{'radio-v'} // "b";
	$templateout->param("CFG_RADIO_V_A", $rv eq "a" ? 1 : 0);
	$templateout->param("CFG_RADIO_V_B", $rv eq "b" ? 1 : 0);
	$templateout->param("CFG_RADIO_V_C", $rv eq "c" ? 1 : 0);

	my $rh = $cfg->{MAIN}{'radio-h'} // "0";
	$templateout->param("CFG_RADIO_H_1", $rh eq "1" ? 1 : 0);
	$templateout->param("CFG_RADIO_H_0", $rh eq "0" ? 1 : 0);

	# --- Select menu: mark the stored value as selected ---------------

	my $sel = $cfg->{MAIN}{select1} // "0";
	$templateout->param("CFG_SELECT1_0", $sel eq "0" ? 1 : 0);
	$templateout->param("CFG_SELECT1_1", $sel eq "1" ? 1 : 0);
	$templateout->param("CFG_SELECT1_2", $sel eq "2" ? 1 : 0);

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
