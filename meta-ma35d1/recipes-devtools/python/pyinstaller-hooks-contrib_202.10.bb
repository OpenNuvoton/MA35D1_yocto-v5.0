SUMMARY = " pyinstaller-hooks-contrib_202.10 "

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=822bee463f4e00ac4478593130e95ccb"


inherit setuptools3

SRC_URI = "git://github.com/pyinstaller/pyinstaller-hooks-contrib.git;protocol=https;branch=master"

SRCREV= "6b9b9412457b9a31c244e3c0601e7c79518e16a7"

S = "${WORKDIR}/git"
B =  "${WORKDIR}/build"

BBCLASSEXTEND = "native nativesdk"
