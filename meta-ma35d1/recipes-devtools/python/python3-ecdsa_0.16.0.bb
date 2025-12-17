SUMMARY = "python3-ecdsa "

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=66ffc5e30f76cbb5358fe54b645e5a1d"

inherit setuptools3 native

SRCREV= "ea9666903c109a8e88a37eb1c60d4e98f01f0299"

SRC_URI = "git://github.com/warner/python-ecdsa.git;protocol=https;branch=master"
S = "${WORKDIR}/git"
B =  "${WORKDIR}/build"

SRC_URI[sha256sum] = "494c6a853e9ed2e9be33d160b41d47afc50a6629b993d2b9c5ad7bb226add892"

BBCLASSEXTEND = "native nativesdk"
