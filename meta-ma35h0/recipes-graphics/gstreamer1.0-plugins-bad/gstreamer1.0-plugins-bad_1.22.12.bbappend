FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI+="file://0001-Add-nufbdevsink-plugin-for-MA35H0-VC8000.patch"

# Adds an ivi_surface role to waylandsink (alongside its existing
# xdg_toplevel path) so it can present under ivi-shell as well as
# kiosk-shell. Only applied on Wayland-enabled distros.
SRC_URI += "${@bb.utils.contains('DISTRO_FEATURES', 'wayland', 'file://0002-waylandsink-ivi-application-support.patch', '', d)}"

# V4L2 stateless decoders (v4l2slh264dec) output dmabuf-backed NV12 with plain
# video/x-raw caps. Let waylandsink accept the dmabuf formats on those caps so
# the decoder output is imported zero-copy via zwp_linux_dmabuf_v1.
SRC_URI += "file://0003-waylandsink-accept-dmabuf-formats-on-system-memory-caps.patch"
