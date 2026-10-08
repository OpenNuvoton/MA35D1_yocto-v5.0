SUMMARY = "GC520 2D HAL (Vivante GC520, Nuvoton MA35D1) - libetna2d"
DESCRIPTION = "Userspace HAL for the Vivante GC520 2D GPU: an opaque C API \
wrapping the GC520 Drawing Engine's bitblt / stretchblt / \
premultiplied-alpha-blend commands on top of libdrm_etnaviv, plus KMS \
scanout helpers. Used by the etnaviv2d Qt5 QPA plugin (qt5-etnaviv2d-qpa)"
LICENSE = "CLOSED"

DEPENDS = "libdrm"

SRC_URI = "git://github.com/OpenNuvoton/MA35D1_Graphics.git;protocol=https;branch=master"
SRCREV = "132e7c81c305bfe9cd5d65c83bb03ffc49cc9594"
S = "${WORKDIR}/git/drm/libetna2d"

EXTRA_OEMAKE = " \
    SYSROOT=${RECIPE_SYSROOT} \
    LIBDRM=${S}/third_party/libdrm-etnaviv-private \
    "

do_install() {
    install -d ${D}${includedir}
    install -m 0644 ${S}/etna2d.h ${D}${includedir}/etna2d.h

    install -d ${D}${libdir}
    install -m 0755 ${S}/build/libetna2d.so.1 ${D}${libdir}/libetna2d.so.1
    ln -sf libetna2d.so.1 ${D}${libdir}/libetna2d.so
}

FILES:${PN} = "${libdir}/libetna2d.so.1"
FILES:${PN}-dev += "${libdir}/libetna2d.so ${includedir}/etna2d.h"

INSANE_SKIP:${PN} += "ldflags"
