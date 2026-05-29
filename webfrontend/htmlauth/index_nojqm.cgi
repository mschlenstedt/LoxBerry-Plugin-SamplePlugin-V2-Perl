#!/usr/bin/perl

# This is the nojqm variant of index.cgi.
# jQuery Mobile is NOT loaded. The page uses the LoxBerry Design System
# (lb-* CSS classes) instead. Pass "nojqm" as the 4th argument to lbheader().
# Use lb-* classes in your templates instead of jQuery Mobile data-role attributes.

##########################################################################
# Modules
##########################################################################

use CGI;
use LoxBerry::System;
use LoxBerry::Web;
use LoxBerry::JSON;
use LoxBerry::Log;
use warnings;
use strict;

##########################################################################
# Variables
##########################################################################

my $cgi = CGI->new;
my $q   = $cgi->Vars;

my $version = LoxBerry::System::pluginversion();
my $template;
my $templateout;
my %L;

# Load plugin config
my $jsonobj = LoxBerry::JSON->new();
my $cfg = $jsonobj->open(filename => "$lbpconfigdir/pluginconfig.json", readonly => 1);

$q->{form} = "main" if !$q->{form};

##########################################################################
# Form dispatch
##########################################################################

if ($q->{form} eq "main") {
	$template = LoxBerry::System::read_file("$lbptemplatedir/index_nojqm.html");
	&form_main();
}
elsif ($q->{form} eq "logs") {
	$template = LoxBerry::System::read_file("$lbptemplatedir/logs.html");
	&form_logs();
}
else {
	$template = LoxBerry::System::read_file("$lbptemplatedir/index_nojqm.html");
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
	return();
}

sub form_logs
{
	&preparetemplate();
	$templateout->param("LOGLIST", LoxBerry::Web::loglist_html());
	return();
}

##########################################################################
# Prepare template
##########################################################################

sub preparetemplate
{
	$templateout = HTML::Template->new_scalar_ref(
		\$template,
		global_vars       => 1,
		loop_context_vars => 1,
		die_on_bad_params => 0,
	);

	%L = LoxBerry::System::readlanguage($templateout, "language.ini");

	our %navbar;

	$navbar{10}{Name}   = "$L{'BASIC.LABEL_PERL_JQM'}";
	$navbar{10}{URL}    = 'index.cgi';

	$navbar{20}{Name}   = "$L{'BASIC.LABEL_PERL_NOJQM'}";
	$navbar{20}{URL}    = 'index_nojqm.cgi';
	$navbar{20}{active} = 1 if $q->{form} eq "main";

	$navbar{30}{Name}   = "$L{'BASIC.LABEL_PHP_JQM'}";
	$navbar{30}{URL}    = 'index_php.php';

	$navbar{40}{Name}   = "$L{'BASIC.LABEL_PHP_NOJQM'}";
	$navbar{40}{URL}    = 'index_php_nojqm.php';

	$navbar{90}{Name}   = "$L{'BASIC.LABEL_LOGS'}";
	$navbar{90}{URL}    = 'index_nojqm.cgi?form=logs';
	$navbar{90}{active} = 1 if $q->{form} eq "logs";

	return();
}

##########################################################################
# Print page
##########################################################################

sub printtemplate
{
	# "nojqm" as 4th parameter: jQuery Mobile is not loaded,
	# LoxBerry Design System (lb-* classes) is used instead.
	LoxBerry::Web::lbheader($L{'BASIC.LABEL_PLUGINTITLE'} . " V$version", "https://wiki.loxberry.de", "help.html", "nojqm");
	print LoxBerry::Log::get_notifications_html($lbpplugindir);
	print $templateout->output();
	LoxBerry::Web::lbfooter();
	return();
}
