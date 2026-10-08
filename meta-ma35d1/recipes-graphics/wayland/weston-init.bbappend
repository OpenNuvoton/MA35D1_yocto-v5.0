FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI += "file://weston-ivi.ini"

# Default Weston launch for the GC520 2D stack: drm-backend + pixman
# software rendering, kiosk-shell by default.
DEFAULTBACKEND = "drm"
PACKAGECONFIG:append = " use-pixman"

# Enable to switch the default shell from kiosk-shell.so to ivi-shell.so
# (+ nu-hmi-controller.so) at build time:
#   PACKAGECONFIG:append:pn-weston-init = " ivi-shell"
PACKAGECONFIG[ivi-shell] = ",,"

do_install:append() {
    sed -i -e "/^\[core\]/a shell=kiosk-shell.so" ${D}${sysconfdir}/xdg/weston/weston.ini

    # Ship both shell configs under /etc/xdg/weston/ so switching shells
    # on-target is always a simple cp:
    #   cp /etc/xdg/weston/weston-kiosk.ini /etc/xdg/weston/weston.ini
    #   cp /etc/xdg/weston/weston-ivi.ini   /etc/xdg/weston/weston.ini
    cp ${D}${sysconfdir}/xdg/weston/weston.ini ${D}${sysconfdir}/xdg/weston/weston-kiosk.ini
    install -D -p -m0644 ${WORKDIR}/weston-ivi.ini ${D}${sysconfdir}/xdg/weston/weston-ivi.ini

    if ${@bb.utils.contains('PACKAGECONFIG', 'ivi-shell', 'true', 'false', d)}; then
        install -m0644 ${D}${sysconfdir}/xdg/weston/weston-ivi.ini ${D}${sysconfdir}/xdg/weston/weston.ini
    fi
}

FILES:${PN} += "${sysconfdir}/xdg/weston/weston-ivi.ini ${sysconfdir}/xdg/weston/weston-kiosk.ini"
CONFFILES:${PN} += "${sysconfdir}/xdg/weston/weston-ivi.ini ${sysconfdir}/xdg/weston/weston-kiosk.ini"
