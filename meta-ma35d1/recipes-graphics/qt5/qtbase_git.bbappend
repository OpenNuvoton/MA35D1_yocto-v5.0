FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

#SRC_URI+="file://linuxfb_doubleubffer.patch"

PACKAGECONFIG:append = " examples tslib linuxfb fontconfig gles2"
PACKAGECONFIG:append = "${@bb.utils.contains('DISTRO_FEATURES', 'directfb', ' directfb', '', d)}"


INSANE_SKIP:${PN}-src += "buildpaths"
INSANE_SKIP:${PN}-examples += "buildpaths"
INSANE_SKIP:${PN}-dev += "buildpaths"

