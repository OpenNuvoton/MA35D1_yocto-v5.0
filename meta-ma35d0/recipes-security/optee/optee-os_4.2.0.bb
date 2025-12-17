require recipes-security/optee/optee-os.inc

DEPENDS += "dtc-native"

FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRCREV = "master"
SRC_URI += " \
    file://0003-optee-enable-clang-support.patch \
   "
