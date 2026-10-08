SUMMARY = "ivi-shell HMI controller plugin for Weston - nu-hmi-controller"
DESCRIPTION = "ivi-shell HMI controller plugin for Weston: assigns \
launch-order-independent layer IDs and z-order to ivi-shell client \
surfaces at runtime (instead of ivi-shell's default launch-order \
stacking). Loaded by Weston via weston.ini's [core] modules= line; \
configured via [nuvoton-layer] sections in weston.ini."
LICENSE = "CLOSED"

DEPENDS = "weston"

SRC_URI = "git://github.com/OpenNuvoton/MA35D1_Graphics.git;protocol=https;branch=master"
SRCREV = "132e7c81c305bfe9cd5d65c83bb03ffc49cc9594"
S = "${WORKDIR}/git/weston/ivi/nu-hmi-controller"

# This BSP's weston recipe is Weston 13.0.1 (libweston-13); point this
# recipe at the correct sysroot paths via WESTON_MAJOR.
WESTON_MAJOR_VERSION = "13"

EXTRA_OEMAKE = " \
    SYSROOT=${RECIPE_SYSROOT} \
    WESTON_MAJOR=${WESTON_MAJOR_VERSION} \
    "

do_install() {
    install -d ${D}${libdir}/weston
    install -m 0755 ${S}/build/nu-hmi-controller.so ${D}${libdir}/weston/nu-hmi-controller.so
}

FILES:${PN} = "${libdir}/weston/nu-hmi-controller.so"
INSANE_SKIP:${PN} += "dev-so ldflags"
