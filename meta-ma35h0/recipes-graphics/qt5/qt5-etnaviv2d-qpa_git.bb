SUMMARY = "Qt5 QPA platform plugin accelerating QPainter through the GC520 2D DE"
DESCRIPTION = "Qt5 QPA (platform abstraction) plugin accelerating QPainter \
fill/blit/blend/stretch through the GC520 2D DE via libetna2d, for direct \
KMS ('composite' mode - no Weston needed) as well as running as a Wayland \
client (linux-dmabuf-v1, xdg_toplevel / ivi_surface, wl_seat input, \
hardware cursor) under Weston. Installs as \
/usr/lib/qt/plugins/platforms/libqetnaviv2d.so; select at runtime with \
QT_QPA_PLATFORM=etnaviv2d[:plane=...]."
LICENSE = "CLOSED"

DEPENDS = "qtbase libetna2d wayland"

# wayland-protocols is not a build dependency - the plugin's Wayland
# protocol bindings are pre-generated and checked into
# src/wayland-protocols/, so there is no wayland-scanner codegen step.

SRC_URI = "git://github.com/OpenNuvoton/MA35D1_Graphics.git;protocol=https;branch=master"
SRCREV = "4249587129a8e396da2b6cc5886b524a6b5bb66a"
PV = "1.1+git${SRCPV}"
S = "${WORKDIR}/git/qt/etnaviv2d-qpa"
inherit qmake5

# Two .pro files live in the source root (the original dev-workflow one,
# and this portable one) - qmake needs an explicit filename.
QMAKE_PROFILES = "${S}/qetnaviv2d.pro"

# Point qetnaviv2d.pro at libetna2d's staged install instead of its
# standalone-build default.
EXTRA_QMAKEVARS_PRE += "ETNA2D_INCDIR=${STAGING_INCDIR} ETNA2D_LIBDIR=${STAGING_LIBDIR}"

FILES:${PN} += "${OE_QMAKE_PATH_PLUGINS}/platforms/libqetnaviv2d.so"
INSANE_SKIP:${PN} += "dev-so buildpaths"

# etnaviv2d_benchmark - a QPainter-based GPU-vs-CPU frame-rate benchmark,
# built once and run with QT_QPA_PLATFORM switched between etnaviv2d/linuxfb
# to compare.
do_compile:append() {
    install -d ${B}/etnaviv2d_benchmark
    cd ${B}/etnaviv2d_benchmark
    ${OE_QMAKE_QMAKE} -makefile -o Makefile ${S}/tests/etnaviv2d_benchmark/etnaviv2d_benchmark.pro \
        || die "qmake failed for etnaviv2d_benchmark"
    oe_runmake -C ${B}/etnaviv2d_benchmark
}

do_install:append() {
    install -d ${D}${bindir}
    install -m 0755 ${B}/etnaviv2d_benchmark/etnaviv2d_benchmark ${D}${bindir}/etnaviv2d_benchmark
}

# Optional demos. Enable with
#   PACKAGECONFIG:append:pn-qt5-etnaviv2d-qpa = " demos"
PACKAGECONFIG ??= ""
PACKAGECONFIG[demos] = ""

do_compile:append() {
    if ${@bb.utils.contains('PACKAGECONFIG', 'demos', 'true', 'false', d)}; then
        install -d ${B}/demos
        cd ${B}/demos
        ${OE_QMAKE_QMAKE} -makefile -o Makefile ${S}/../demos/demos.pro \
            || die "qmake failed for demos"
        oe_runmake -C ${B}/demos
    fi
}

do_install:append() {
    if ${@bb.utils.contains('PACKAGECONFIG', 'demos', 'true', 'false', d)}; then
        install -d ${D}${bindir}
        install -m 0755 ${B}/demos/cockpit/cockpit ${D}${bindir}/cockpit
        install -m 0755 ${B}/demos/dashboard/dashboard ${D}${bindir}/dashboard
    fi
}
