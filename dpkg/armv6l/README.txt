# dpkg/armv6l/ - Architecture-specific .deb packages for ARMv6l (32-bit).
#
# Place any .deb package files for Raspberry Pi 1 and Zero (ARMv6) here.
# LoxBerry installs all *.deb files in this directory via "dpkg -i -R" during
# plugin installation, but only on systems where "uname -m" returns "armv6l".
#
# Only use this for packages that are NOT available in the standard Debian
# repository (dpkg/apt). Prefer apt whenever possible.
#
# This README.txt file is ignored by the installer (only *.deb files are processed).
