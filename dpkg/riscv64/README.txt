# dpkg/riscv64/ - Architecture-specific .deb packages for RISC-V 64-bit.
#
# Place any .deb package files for riscv64 systems here.
# LoxBerry installs all *.deb files via "dpkg -i -R" during plugin installation,
# but only on systems where "uname -m" returns "riscv64".
#
# Only use this for packages that are NOT available in the standard Debian
# repository (dpkg/apt). Prefer apt whenever possible.
#
# This README.txt file is ignored by the installer (only *.deb files are processed).
