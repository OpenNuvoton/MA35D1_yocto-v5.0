FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

PACKAGECONFIG:append = " examples tslib linuxfb fontconfig"
PACKAGECONFIG:append = "${@bb.utils.contains('DISTRO_FEATURES', 'directfb', ' directfb', '', d)}"

# gles2 (egl) only for distros with opengl enabled (e.g. weston)
PACKAGECONFIG:append = "${@bb.utils.contains('DISTRO_FEATURES', 'opengl', ' gles2', '', d)}"

INSANE_SKIP:${PN}-src += "buildpaths"
INSANE_SKIP:${PN}-examples += "buildpaths"
INSANE_SKIP:${PN}-dev += "buildpaths"

