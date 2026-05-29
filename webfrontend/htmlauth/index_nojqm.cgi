#!/usr/bin/perl

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

my $log;

# Read form parameters
my $cgi = CGI->new;
my $q = $cgi->Vars;

my $version = LoxBerry::System::pluginversion();
my $template;
my $templatefile;
my $templateout;

# Language phrases
my %L;

# Load plugin config
my $cfgfile = "$lbpconfigdir/pluginconfig.json";
my $jsonobj = LoxBerry::JSON->new();
my $cfg = $jsonobj->open(filename => $cfgfile, readonly => 1);

# Default form
$q->{form} = "main" if !$q->{form};

##########################################################################
# Form dispatch
##########################################################################

if ($q->{form} eq "main") {
	$templatefile = "$lbptemplatedir/index.html";
	$template = LoxBerry::System::read_file($templatefile);
	&form_main();
}
elsif ($q->{form} eq "logs") {
	$templatefile = "$lbptemplatedir/index.html";
	$template = LoxBerry::System::read_file($templatefile);
	&form_logs();
}
else {
	$templatefile = "$lbptemplatedir/index.html";
	$template = LoxBerry::System::read_file($templatefile);
	&form_main();
}

&printtemplate();
exit;

##########################################################################
# Form: Main settings
##########################################################################

sub form_main
{
	&preparetemplate();
	return();
}

##########################################################################
# Form: Log viewer
##########################################################################

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
		global_vars => 1,
		loop_context_vars => 1,
		die_on_bad_params => 0,
	);

	# Language file
	%L = LoxBerry::System::readlanguage($templateout, "language.ini");

	# Navbar
	our %navbar;

	$navbar{10}{Name}   = "$L{'BASIC.LABEL_MAIN'}";
	$navbar{10}{URL}    = 'index_nojqm.cgi?form=main';
	$navbar{10}{active} = 1 if $q->{form} eq "main";

	$navbar{90}{Name}   = "$L{'BASIC.LABEL_LOGS'}";
	$navbar{90}{URL}    = 'index_nojqm.cgi?form=logs';
	$navbar{90}{active} = 1 if $q->{form} eq "logs";

	return();
}

##########################################################################
# Print template with LoxBerry header and footer (nojqm mode)
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
