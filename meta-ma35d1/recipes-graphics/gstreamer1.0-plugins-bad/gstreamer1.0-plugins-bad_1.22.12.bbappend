FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI+="file://0001-Add-nufbdevsink-plugin-for-MA35D1-VC8000.patch"

# Adds an ivi_surface role to waylandsink (alongside its existing
# xdg_toplevel path) so it can present under ivi-shell as well as
# kiosk-shell. Only applied on Wayland-enabled distros.
SRC_URI += "${@bb.utils.contains('DISTRO_FEATURES', 'wayland', 'file://0002-waylandsink-ivi-application-support.patch', '', d)}"
