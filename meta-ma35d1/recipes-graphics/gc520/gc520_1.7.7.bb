SUMMARY = "GC520 library for DirectFB"
DEPENDS = "directfb"
SECTION = "libs"
LICENSE = "CLOSED"

RV = "1.7-7"

SRC_URI += " \
    file://libdirectfb_gal.so \
    file://libGAL.so \
    file://galcore.ko_${KERNEL_VERSION} \
    "
do_package_qa[noexec] = "1"
do_install() {
    install -d ${D}/${libdir}/directfb-${RV}/gfxdrivers/
    install -d ${D}/${libdir}/
    install -m 0755 ${WORKDIR}/libdirectfb_gal.so ${D}/${libdir}/directfb-${RV}/gfxdrivers/libdirectfb_gal.so
    install -m 0755 ${WORKDIR}/libGAL.so ${D}/${libdir}/libGAL.so

    install -d ${D}/${base_libdir}/modules/${KERNEL_VERSION}
    install -m 0644 ${WORKDIR}/galcore.ko_${KERNEL_VERSION} \
		${D}/${base_libdir}/modules/${KERNEL_VERSION}/galcore.ko
}

FILES:SOLIBSDEV = ""
FILES:${PN} = "${libdir}/directfb-${RV}/gfxdrivers/libdirectfb_gal.so ${libdir}/libGAL.so ${base_libdir}/modules/${KERNEL_VERSION}/galcore.ko"
PACKAGE:ARCH = "${MACHINE_ARCH}"
COMPATIBLE:MACHINE = "(ma35d1)"
