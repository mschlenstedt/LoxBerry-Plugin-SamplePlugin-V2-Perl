# dpkg/aarch64/ - Architecture-specific .deb packages for AArch64 / ARM64 (64-bit).
#
# Place any .deb package files for Raspberry Pi 2, 3, 4, 5 and Zero 2 running
# a 64-bit OS here. LoxBerry installs all *.deb files via "dpkg -i -R" during
# plugin installation, but only on systems where "uname -m" returns "aarch64".
#
# Only use this for packages that are NOT available in the standard Debian
# repository (dpkg/apt). Prefer apt whenever possible.
#
# This README.txt file is ignored by the installer (only *.deb files are processed).
