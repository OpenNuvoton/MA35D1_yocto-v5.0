SUMMARY = " pyinstaller_4.00 "

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://COPYING.txt;md5=9026c0c1a28526b6ed7e4dce6423fbd7"
inherit setuptools3 native

SRCREV= "30e13d63f2c93af0d8a11fcfeeb1a182e316239d"

SRC_URI = "git://github.com/pyinstaller/pyinstaller.git;protocol=https;branch=v5"
S = "${WORKDIR}/git"
B =  "${WORKDIR}/build"

BBCLASSEXTEND = "native nativesdk"

INHIBIT_SYSROOT_STRIP = "1"
INSANK_SKIP_${PN}:append = "already-stripped"
