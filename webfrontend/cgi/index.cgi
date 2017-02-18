#!/usr/bin/perl

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


##########################################################################
# Modules
##########################################################################

use CGI::Carp qw(fatalsToBrowser);
use CGI qw/:standard/;
use Config::Simple;
use File::HomeDir;
use String::Escape qw( unquotemeta );
use Cwd 'abs_path';
use HTML::Template;
use warnings;
use strict;

##########################################################################
# Variables
##########################################################################
my  $cgi = new CGI;
my  $cfg;
my  $plugin_cfg;
my  $lang;
my  $installfolder;
my  $languagefile;
my  $version;
my  $home = File::HomeDir->my_home;
my  $psubfolder;
my  $pname;
my  $languagefileplugin;
my  %TPhrases;

##########################################################################
# Read Settings
##########################################################################

# Version of this script
$version = "0.1";

# Figure out in which subfolder we are installed
$psubfolder = abs_path($0);
$psubfolder =~ s/(.*)\/(.*)\/(.*)$/$2/g;

# Start with HTML header
print $cgi->header('text/html'); 

# Read general config
$cfg	 	= new Config::Simple("$home/config/system/general.cfg") or die $cfg->error();
$installfolder	= $cfg->param("BASE.INSTALLFOLDER");
$lang		= $cfg->param("BASE.LANG");

# Read plugin config
$plugin_cfg 	= new Config::Simple("$installfolder/config/plugins/$psubfolder/pluginconfig.cfg") or die $plugin_cfg->error();
$pname          = $plugin_cfg->param("MAIN.SCRIPTNAME");

# Set parameters coming in - get over post
if ( $cgi->param('lang') ) {
	$lang = quotemeta( $cgi->param('lang') );
}
elsif ( $cgi->url_param('lang') ) {
	$lang = quotemeta( $cgi->url_param('lang') );
}

##########################################################################
# Initialize html templates
##########################################################################

# See http://www.perlmonks.org/?node_id=65642

# Header # At the moment not in HTML::Template format
#$headertemplate = HTML::Template->new(
#	filename => "$installfolder/templates/system/$lang/header.html",
#	die_on_bad_params => 0,
#	associate => $cgi,
#);

# Main
#$maintemplate = HTML::Template->new(filename => "$installfolder/templates/plugins/$psubfolder/multi/main.html");
$maintemplate = HTML::Template->new(
	filename => "$installfolder/templates/plugins/$psubfolder/multi/main.html",
	die_on_bad_params => 0,
	associate => $cgi,
);


# Footer # At the moment not in HTML::Template format
#$footertemplate = HTML::Template->new(
#	filename => "$installfolder/templates/system/$lang/footer.html",
#	die_on_bad_params => 0,
#	associate => $cgi,
#);

##########################################################################
# Translations
##########################################################################

# Init Language
# Clean up lang variable
$lang         =~ tr/a-z//cd;
$lang         = substr($lang,0,2);

# Read Plugin transations
# Read English language as default
# Missing phrases in foreign language will fall back to English
$languagefileplugin 	= "$installfolder/templates/plugins/$psubfolder/en/language.txt";
Config::Simple->import_from($languagefileplugin, \%TPhrases);

# Read foreign language if exists and not English
$languagefileplugin = "$installfolder/templates/plugins/$psubfolder/$lang/language.txt";
# Now overwrite phrase variables with user language
if ((-e $languagefileplugin) and ($lang ne 'en')) {
	Config::Simple->import_from($languagefileplugin, \%TPhrases);
}

# Parse phrase variables to html templates
while (my ($name, $value) = each %TPhrases){
	$maintemplate->param("T::$name" => $value);
	#$headertemplate->param("T::$name" => $value);
	#$footertemplate->param("T::$name" => $value);
}


##########################################################################
# Print Template
##########################################################################

# Header
#print $headertemplate->output;

# Main
print $maintemplate->output;

# Footer
#print $footertemplate->output;

exit;
