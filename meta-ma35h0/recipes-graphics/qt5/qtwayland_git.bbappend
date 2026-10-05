FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

# Not used by this stack (the etnaviv2d QPA plugin talks raw
# libwayland-client directly, and Weston is a C/libweston compositor, not
# QtWayland/QML). Kept available with this build-time fix (X11-less
# sysroot) in case a future QtQuick-based Wayland compositor is added.
SRC_URI += "file://0001-compositor-wayland-egl-define-QT_EGL_NO_X11-for-no-X.patch"
