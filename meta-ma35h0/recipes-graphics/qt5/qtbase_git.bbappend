FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

#SRC_URI+="file://linuxfb_doubleubffer.patch"

PACKAGECONFIG:append = " examples directfb tslib linuxfb fontconfig gles2"


INSANE_SKIP:${PN}-src += "buildpaths"
INSANE_SKIP:${PN}-examples += "buildpaths"
INSANE_SKIP:${PN}-dev += "buildpaths"

